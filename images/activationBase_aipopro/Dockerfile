FROM busybox

RUN mkdir -p /activationBase

COPY data/preprocessed/activation_data.csv /activationBase/
COPY README.md /activationBase/

CMD ["sh", "-c", "mkdir -p /tmp && cp -r /activationBase /tmp/"]

