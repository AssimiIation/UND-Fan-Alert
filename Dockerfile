FROM python:3-slim-bookworm
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD und_fan_alert.py config.yml /
CMD [ "python", "./und_fan_alert.py"]