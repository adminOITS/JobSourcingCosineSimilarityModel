import json
import logging
from matching import calculate_all_matching_scores
from matching import calculate_total_match_score
import boto3
import requests
from boto3.dynamodb.conditions import Key
import boto3
from datetime import datetime
from mappers import (
    map_job_offer_response_dto,
    map_profile_response_dto
)

ssm = boto3.client("ssm")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("MatchingResults")

def store_result_in_dynamodb(offer_id, profile_id, candidate_id, scores: dict, status: str):
    now = datetime.utcnow().isoformat()
    
    # Use your new weighting logic here
    total_match = calculate_total_match_score(scores=scores)

    response = table.update_item(
        Key={
            'offerId': offer_id,
            'profileId': profile_id
        },
        UpdateExpression="""
            SET 
                candidateId = :cid,
                status = :status,
                matchDetails = :md,
                totalMatch = :tm,
                updatedAt = :upd,
                createdAt = if_not_exists(createdAt, :cre)
        """,
        ExpressionAttributeValues={
            ':cid': candidate_id,
            ':status': status,
            ':md': scores,
            ':tm': total_match,
            ':upd': now,
            ':cre': now
        },
        ReturnValues="UPDATED_NEW"
    )

    logger.info(f"DynamoDB update response: {json.dumps(response)}")



def get_parameter(name, with_decryption=False):
    return ssm.get_parameter(Name=name, WithDecryption=with_decryption)["Parameter"]["Value"]



def fetch_offer_dto(gateway_url, headers ,offer_id):
    url = f"{gateway_url}/OFFER-SERVICE/api/v1/offers/{offer_id}/matching"
    logger.info(f"Fetching offer from: {url}")
    response = requests.get(url,headers=headers, timeout=30)
    response.raise_for_status()
    return response

def fetch_profile_dto(gateway_url,headers ,candidate_id ,profile_id):
    url = f"{gateway_url}/PROFILE-SERVICE/api/v1/candidates/{candidate_id}/profiles/{profile_id}/matching"
    logger.info(f"Fetching profile from: {url}")
    response = requests.get(url,headers=headers, timeout=30)
    response.raise_for_status()
    return response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_access_token():
    token_url = "https://job-sourcing.com/realms/jobsourcingrealm/protocol/openid-connect/token"
    client_id = "lamdaParsingAiClient"
    client_secret = CLIENT_SECRET_KEYCLOAK

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(token_url, data=data)
    response.raise_for_status()

    return response.json()["access_token"]


CLIENT_SECRET_KEYCLOAK=get_parameter("/llama/client_secret_keycloak", with_decryption=True)
gateway_url = get_ssm_param("/jobsourcing/env/dev/gateway/url")

def lambda_handler(event, context):
    """
    AWS Lambda entry point triggered by SQS messages (batch size = 1).
    Each message must contain a JSON object with:
    {
        "offerDto": { ... },
        "profileDto": { ... }
    }
    """
    try:
        # Expecting a single record in batch (batchSize = 1)
        record = event['Records'][0]
        body = json.loads(record['body'])

        offer_id = body.get("offerId")
        profile_id = body.get("profileId")
        candidate_id = body.get("candidateId")
        total_profiles = body.get("totalProfile")

        # Validate presence of all required fields
        missing_fields = []
        if not offer_id:
            missing_fields.append("offerId")
        if not profile_id:
            missing_fields.append("profileId")
        if not candidate_id:
            missing_fields.append("candidateId")
        if total_profiles is None:
            missing_fields.append("totalProfile")

        if missing_fields:
            raise ValueError(f"Missing required fields in message: {', '.join(missing_fields)}")

        token = get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        offer_json = fetch_offer_dto(gateway_url, headers ,offer_id)
        profile_json = fetch_profile_dto(gateway_url,headers ,candidate_id ,profile_id)

        if not offer_json or not profile_json:
            logger.error("Missing 'offerDto' or 'profileDto' in the payload")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields"})
            }

        # Map to DTOs
        offer_dto = map_job_offer_response_dto(offer_json)
        profile_dto = map_profile_response_dto(profile_json)

        # Calculate scores
        result = calculate_all_matching_scores(offer_dto, profile_dto)

        logger.info(f"Matching result: {json.dumps(result)}")


        store_result_in_dynamodb(
                offer_id=offer_id,
                profile_id=profile_id,
                candidate_id=candidate_id,
                scores=result,
                status="COMPLETED"
            )
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    except Exception as e:
        logger.exception("Error during Lambda execution")
        # Extract IDs if available to log failure
        offer_id = body.get("offerId")
        profile_id = body.get("profileId")
        candidate_id = body.get("candidateId", "UNKNOWN")

        # Only store in DynamoDB if both IDs are available
        if offer_id and profile_id:
            store_result_in_dynamodb(
                offer_id=offer_id,
                profile_id=profile_id,
                candidate_id=candidate_id,
                scores={},  # No scores on failure
                status="FAILED"
            )
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
