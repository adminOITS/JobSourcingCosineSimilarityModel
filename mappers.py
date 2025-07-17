from typing import List
from dto import (
    CandidateSkillResponseDto,
    JobOfferSkillResponseDto,
    SkillProficiencyLevel,
    OfferProficiencyLevel,
    RequirementLevel,
    JobOfferExperienceResponseDto,
    CandidateExperienceResponseDto,
    JobOfferEducationResponseDto,
    CandidateEducationResponseDto,
    JobOfferLanguageResponseDto,
    CandidateLanguageResponseDto,
    LanguageProficiencyLevel,
    AddressResponseDto,
    CandidateResponseDto,
    ProfileResponseDto,
    JobOfferResponseDto,
)

def map_candidate_skills(skills_data: List[dict]) -> List[CandidateSkillResponseDto]:
    return [
        CandidateSkillResponseDto(
            name=skill["name"],
            proficiencyLevel=SkillProficiencyLevel(skill["proficiencyLevel"].upper())
        )
        for skill in skills_data
    ]

def map_offer_skills(skills_data: List[dict]) -> List[JobOfferSkillResponseDto]:
    return [
        JobOfferSkillResponseDto(
            skillName=skill["skillName"],
            proficiency=OfferProficiencyLevel(skill["proficiency"].upper()),
            requirementLevel=RequirementLevel(skill["requirementLevel"].upper())
        )
        for skill in skills_data
    ]

def map_offer_experiences(data: List[dict]) -> List[JobOfferExperienceResponseDto]:
    return [
        JobOfferExperienceResponseDto(
            title=item.get("title", ""),
            companyName=item.get("companyName"),
            description=item.get("description"),
            yearsRequired=item.get("yearsRequired"),
            requirementLevel=RequirementLevel(item.get("requirementLevel", "OPTIONAL"))
        )
        for item in data
    ]

def map_candidate_experiences(data: List[dict]) -> List[CandidateExperienceResponseDto]:
    return [
        CandidateExperienceResponseDto(
            jobTitle=item.get("jobTitle", ""),
            company=item.get("company"),
            startDate=item.get("startDate"),
            endDate=item.get("endDate"),
            isCurrent=item.get("isCurrent", False),
            description=item.get("description"),
            location=item.get("location"),
            industry=item.get("industry")
        )
        for item in data
    ]

def map_offer_educations(data: List[dict]) -> List[JobOfferEducationResponseDto]:
    return [
        JobOfferEducationResponseDto(
            degree=item.get("degree", "").strip(),
            field=item.get("field"),
            institution=item.get("institution"),
            requirementLevel=RequirementLevel(item.get("requirementLevel", "OPTIONAL")),
            description=item.get("description")
        )
        for item in data
    ]

def map_candidate_educations(data: List[dict]) -> List[CandidateEducationResponseDto]:
    return [
        CandidateEducationResponseDto(
            degree=item.get("degree", "").strip(),
            field=item.get("field"),
            institution=item.get("institution"),
            startDate=item.get("startDate"),
            endDate=item.get("endDate"),
            isCurrent=item.get("isCurrent", False),
            location=item.get("location")
        )
        for item in data
    ]

def map_offer_languages(data: List[dict]) -> List[JobOfferLanguageResponseDto]:
    return [
        JobOfferLanguageResponseDto(
            language=lang["language"],
            proficiency=LanguageProficiencyLevel[lang["proficiency"]],
            requirementLevel=RequirementLevel[lang["requirementLevel"]]
        )
        for lang in data
    ]

def map_candidate_languages(data: List[dict]) -> List[CandidateLanguageResponseDto]:
    return [
        CandidateLanguageResponseDto(
            language=lang["language"],
            proficiencyLevel=LanguageProficiencyLevel[lang["proficiencyLevel"]]
        )
        for lang in data
    ]

def map_address(data: dict) -> AddressResponseDto:
    return AddressResponseDto(
        addressLine1=data.get("addressLine1", ""),
        addressLine2=data.get("addressLine2", ""),
        city=data.get("city", ""),
        state=data.get("state", ""),
        zipCode=data.get("zipCode", ""),
        country=data.get("country", "")
    )

def map_candidate_response_dto(data: dict) -> CandidateResponseDto:
    return CandidateResponseDto(
        address=map_address(data.get("address", {})),
        experiences=map_candidate_experiences(data.get("experiences", [])),
        education=map_candidate_educations(data.get("education", [])),
        languages=map_candidate_languages(data.get("languages", []))
    )

def map_profile_response_dto(data: dict) -> ProfileResponseDto:
    return ProfileResponseDto(
        profileTitle=data.get("profileTitle", ""),
        category=data.get("category"),
        candidate=map_candidate_response_dto(data.get("candidate", {})),
        skills=map_candidate_skills(data.get("skills", [])),
    )

def map_job_offer_response_dto(data: dict) -> JobOfferResponseDto:
    return JobOfferResponseDto(
        title=data.get("title", ""),
        category=data.get("category"),
        city=data.get("city"),
        country=data.get("country"),
        zipCode=data.get("zipCode"),
        skills=map_offer_skills(data.get("skills", [])),
        experiences=map_offer_experiences(data.get("experiences", [])),
        educations=map_offer_educations(data.get("educations", [])),
        languages=map_offer_languages(data.get("languages", []))
    )
