FROM rabbitmq:3.8.16-management

COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

CMD rabbitmq-server