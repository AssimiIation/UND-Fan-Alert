FROM python:3.11-slim-bookworm
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD und_fan_alert.py config/config.yml /
CMD [ "python3", "./und_fan_alert.py"]