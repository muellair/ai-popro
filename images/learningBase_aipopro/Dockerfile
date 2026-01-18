FROM busybox

RUN mkdir -p learningBase/train \
             learningBase/validation

# copy data to /learningBase instead of /tmp/learningBase so that not deleted when mounting volume
COPY data/preprocessed/training_data.csv learningBase/train/
COPY data/preprocessed/test_data.csv learningBase/validation/
CMD ["sh", "-c" ,"cp learningBase/train/training_data.csv /tmp/train/ && cp learningBase/validation/test_data.csv /tmp/validation/"]
