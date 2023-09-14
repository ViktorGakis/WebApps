# FROM debian:bullseye-slim
FROM ubuntu:latest

LABEL maintainer="Anaconda, Inc"

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8


# Install required packages
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
    bzip2 \
    ca-certificates \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    mercurial \
    openssh-client \
    procps \
    subversion \
    wget \
    git \
    g++ \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g n
RUN n stable
RUN npm -g install create-react-app

# Set environment variables
ENV MINICONDA_VERSION=latest
ENV CONDA_DIR=/opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
ENV CONDA_ENV=denv

COPY requirements.txt .

CMD [ "/bin/bash" ]

RUN set -x && \
    UNAME_M="$(uname -m)" && \
    if [ "${UNAME_M}" = "x86_64" ]; then \
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh"; \
    SHA256SUM="634d76df5e489c44ade4085552b97bebc786d49245ed1a830022b0b406de5817"; \
    elif [ "${UNAME_M}" = "s390x" ]; then \
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-s390x.sh"; \
    SHA256SUM="221a4cd7f0a9275c3263efa07fa37385746de884f4306bb5d1fe5733ca770550"; \
    elif [ "${UNAME_M}" = "aarch64" ]; then \
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-aarch64.sh"; \
    SHA256SUM="3962738cfac270ae4ff30da0e382aecf6b3305a12064b196457747b157749a7a"; \
    elif [ "${UNAME_M}" = "ppc64le" ]; then \
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-ppc64le.sh"; \
    SHA256SUM="92237cb2a443dd15005ec004f2f744b14de02cd5513a00983c2f191eb43d1b29"; \
    fi && \
    wget "${MINICONDA_URL}" -O miniconda.sh -q && \
    echo "${SHA256SUM} miniconda.sh" > shasum && \
    if [ "${MINICONDA_VERSION}" != "latest" ]; then sha256sum --check --status shasum; fi && \
    mkdir -p /opt && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh shasum && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy

# Add Conda Forge channel
RUN conda config --add channels conda-forge

RUN conda update conda


# Update conda and create a default environment
RUN conda update -n base -c defaults conda && \
    conda create -n $CONDA_ENV python=3.11 && \
    conda clean -afy

# RUN conda init bash

RUN /opt/conda/bin/conda run -n $CONDA_ENV conda install --file requirements.txt


# Activate the denv environment
# RUN conda activate ${CONDA_ENV} && \
#     conda install --file requirements.txt

# RUN echo "conda activate ${CONDA_ENV}" >> /etc/profile.d/conda.sh && \
# SHELL ["/bin/bash", "-c"]

# Install packages from requirements.txt

# Install packages from requirements.txt
# RUN conda install --file requirements.txt

# Define the working directory
WORKDIR /app

# Copy the application contents for git push
# COPY interface.py .
# COPY interface/ ./interface
# COPY scraper.ipynb .
# COPY test.py .


# Switch to a non-root user
# Set up Conda environment
# RUN useradd --uid 1000 theios && \
#     mkdir -p /home/theios && \
#     chown -R theios /app /home/theios "${CONDA_DIR}"

# USER theios

# Add Conda init to .bashrc
# RUN echo ". ${CONDA_DIR}/etc/profile.d/conda.sh" >> /root/.bashrc && \
#     echo "conda activate ${CONDA_ENV}" >> /root/.bashrc


EXPOSE 8080
