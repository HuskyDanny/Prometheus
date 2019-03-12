FROM python:3.6-alpine
Run mkdir -p /usr/src/app
Workdir /usr/src/app
Copy . .
RUN pip install prometheus_client
RUN pip install requests
RUN pip install flask
RUN pip install wtforms
EXPOSE 80
CMD ["python", "./main.py"]