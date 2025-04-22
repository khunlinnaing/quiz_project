FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    default-libmysqlclient-dev \
    libgl1-mesa-glx \  
    libglib2.0-0 && \  
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 9000
CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]