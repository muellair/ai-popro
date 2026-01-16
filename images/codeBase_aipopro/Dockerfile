FROM busybox

# Install Python manually
RUN mkdir -p /usr/local/bin
ADD https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.10.13+20240107-x86_64-unknown-linux-gnu-install_only.tar.gz /tmp/python.tar.gz
RUN tar -xzf /tmp/python.tar.gz -C /usr/local --strip-components=1

ENV PATH=/usr/local/bin:/home/thinkpad/miniconda3/condabin:/home/thinkpad/.local/bin:/home/thinkpad/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin

# Create code directory
RUN mkdir -p /codeBase

# Copy evaluation script
COPY src/evaluate.py /codeBase/
COPY README.md /codeBase/

CMD [sh]

