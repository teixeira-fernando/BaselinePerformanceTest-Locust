FROM locustio/locust:2.7.3
RUN pip3 install python-dotenv
RUN pip3 install locust-plugins