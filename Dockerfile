FROM  python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./dvmn_bot/requirements.txt /dvmn_bot/requirements.txt
RUN pip install -r /dvmn_bot/requirements.txt
WORKDIR /dvmn_bot
COPY ./dvmn_bot /dvmn_bot


CMD ["python", "main.py"]
