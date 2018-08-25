FROM python:3.5
COPY . /
RUN pip install -r requirements.txt
CMD python bot.py