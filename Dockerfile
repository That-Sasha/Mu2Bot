FROM python:3.9.22-bookworm

WORKDIR /usr/src/app

ADD mu2bot/ mu2bot

WORKDIR mu2bot

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "mu2bot.py"]