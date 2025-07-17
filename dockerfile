FROM public.ecr.aws/lambda/python:3.11

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Install OS-level build dependencies
RUN yum update -y && \
    yum groupinstall -y "Development Tools" && \
    yum install -y \
        gcc \
        gcc-c++ \
        python3-devel \
        atlas-devel \
        blas-devel \
        lapack-devel \
        openblas-devel \
        libffi-devel \
        findutils \
    && yum clean all

# Copy source files and requirements
COPY requirements.txt ./
COPY app.py dto.py mappers.py matching.py ./

# Install Python packages
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Define Lambda entrypoint
CMD ["app.lambda_handler"]
