FROM python:3.9.22-bookworm

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY mu2bot.py ./

CMD ["python", "./mu2bot.py"]