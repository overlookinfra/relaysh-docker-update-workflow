FROM relaysh/core:python-latest
COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
