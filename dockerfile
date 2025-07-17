# Use AWS Lambda Python 3.11 base image
FROM public.ecr.aws/lambda/python:3.11

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Install OS-level build tools needed by numpy, scikit-learn
RUN yum -y install gcc gcc-c++ make python3-devel libffi-devel

# Copy all app files
COPY requirements.txt ./
COPY app.py dto.py mappers.py matching.py ./

# Install Python packages
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Set Lambda entrypoint
CMD ["app.lambda_handler"]
