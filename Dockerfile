FROM python:3.9-slim

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

RUN  python3 app/download_model.py


EXPOSE 8501


CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]