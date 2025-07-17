# Use the official AWS Lambda Python 3.11 image
FROM public.ecr.aws/lambda/python:3.11

# Install build tools and required system packages
RUN yum -y install gcc gcc-c++ python3-devel && yum clean all

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy source files
COPY requirements.txt ./
COPY app.py dto.py mappers.py matching.py ./

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Lambda handler
CMD ["app.lambda_handler"]
