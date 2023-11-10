#!/bin/bash

# No effect for this
# tsting for change guest guest  

# Start RabbitMQ
rabbitmq-server -detached

# Wait for RabbitMQ to start
sleep 2

# Change the default user and password
rabbitmqctl change_password guest ${AMQP_PASSWORD}
rabbitmqctl rename_user guest ${AMQP_USER}

# Stop RabbitMQ
rabbitmqctl stop

# Start RabbitMQ in foreground
rabbitmq-server