FROM python:alpine3.17

WORKDIR ./app
COPY . .

RUN pip install requests
RUN pip install flask
RUN pip install flask_restful
RUN pip install blabaldbsdfbsfbfdbfababfdbafdb

EXPOSE 8000
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=8000

CMD ["flask", "run", "--host=0.0.0.0"]
