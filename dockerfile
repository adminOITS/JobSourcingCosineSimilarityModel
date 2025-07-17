# Use the official AWS Lambda Python 3.11 image
FROM public.ecr.aws/lambda/python:3.11

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy all source files
COPY requirements.txt ./
COPY app.py dto.py mappers.py matching.py ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Define Lambda handler entry point (file.function)
CMD ["app.lambda_handler"]






