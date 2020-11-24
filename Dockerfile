From python:3.7-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends unzip wget && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb ; apt-get -fy install && \
    wget https://chromedriver.storage.googleapis.com/87.0.4280.20/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mkdir browserDriver && mv chromedriver /browserDriver && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f google-chrome-stable_current_amd64.deb && \
    rm -f chromedriver_linux64.zip

ENV PATH=/browserDriver:$PATH

RUN pip install --no-cache-dir selenium==3.141.0

ENTRYPOINT ["/bin/bash"]
