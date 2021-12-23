FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8080
ENV FLASK_APP app.py
ENV FLASK_ENV development

CMD ["flask","run","--host=0.0.0.0","--port=8080"]

