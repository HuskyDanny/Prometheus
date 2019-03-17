FROM python:3.6-alpine
Run mkdir -p /usr/src/app
Workdir /usr/src/app
Copy . .
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "./main.py"]
