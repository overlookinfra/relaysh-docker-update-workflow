FROM relaysh/core:latest-python
COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
