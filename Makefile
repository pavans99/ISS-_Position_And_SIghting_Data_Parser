NAME ?= pavanshukla99

all: build run push

images:
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}

build:
	docker build -t ${NAME}/midterm:latest .

run:
	docker run --name "midterm" -d -p 5030:5000 ${NAME}/midterm:latest

push:
	docker push ${NAME}/midterm:latest
