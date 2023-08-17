FROM locustio/locust:latest
RUN pip3 install python-dotenv
RUN pip3 install locust-plugins