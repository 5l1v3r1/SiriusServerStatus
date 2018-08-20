FROM python:3.5
COPY . /bot
CMD pip install -r /bot/requirements.txt
CMD python /bot/bot.py