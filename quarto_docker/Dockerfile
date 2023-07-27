FROM amd64/ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    pip \
    ca-certificates \
    curl \
    gdebi-core \
    libfontconfig \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LO https://github.com/quarto-dev/quarto-cli/releases/download/v1.2.269/quarto-1.2.269-linux-amd64.deb
RUN gdebi --non-interactive quarto-1.2.269-linux-amd64.deb

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN quarto install tinytex