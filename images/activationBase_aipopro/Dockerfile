FROM busybox

RUN mkdir -p /activationBase

COPY data/preprocessed/activation_data.csv /activationBase/
COPY images/activationBase_aipopro/Readme.md /activationBase/

CMD ["sh", "-c", "mkdir -p /tmp && cp -r /activationBase /tmp/"]

