FROM python:3.14-slim-bookworm

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    HOME=/tmp/rotec-home JUPYTER_RUNTIME_DIR=/tmp/jupyter-runtime \
    MPLCONFIGDIR=/tmp/matplotlib \
    OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-noto-cjk libgomp1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /opt/rotec/requirements.txt
RUN python -m pip install --no-cache-dir -r /opt/rotec/requirements.txt \
    && python -m pip check
COPY 한국로텍_데이터분석.ipynb /opt/rotec/한국로텍_데이터분석.ipynb
COPY docker/ /opt/rotec/docker/
COPY scripts/run_notebook.py /opt/rotec/run_notebook.py
RUN mkdir -p /workspace && chmod 1777 /workspace
WORKDIR /workspace
USER 1000:1000
EXPOSE 8888
ENTRYPOINT ["python", "/opt/rotec/docker/start.py"]
