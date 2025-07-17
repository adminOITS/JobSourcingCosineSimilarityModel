# Use the official AWS Lambda Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.11

# Copy the requirements file into the container
COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY LmabdaParsingCode.py ${LAMBDA_TASK_ROOT}

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt



# Command to run the Lambda function
CMD ["app.lambda_handler"]
