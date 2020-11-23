FROM python:slim
RUN pip --no-cache-dir install requests lxml
ENTRYPOINT ["/bin/bash"]