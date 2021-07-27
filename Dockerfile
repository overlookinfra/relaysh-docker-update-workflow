FROM python:3-alpine

ARG cli=v4.5.0
RUN set -eux ; \
   wget https://github.com/puppetlabs/relay/releases/download/${cli}/relay-${cli}-linux-amd64 && \
   wget https://github.com/puppetlabs/relay/releases/download/${cli}/relay-${cli}-linux-amd64.sha256 && \
   echo "$( cat relay-${cli}-linux-amd64.sha256 )  relay-${cli}-linux-amd64" | sha256sum -c - && \
   mv relay-${cli}-linux-amd64 /usr/local/bin/relay && chmod 755 /usr/local/bin/relay && \
   rm relay-${cli}-linux-amd64.sha256

RUN pip --no-cache-dir install pyyaml

COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
