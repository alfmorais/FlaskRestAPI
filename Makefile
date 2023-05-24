build-no-cache:
	sudo docker build -t rest-api . --no-cache

build:
	sudo docker build -t rest-api .

run:
	sudo docker run -dp 5002:5000 -w /app -v "$(pwd):/app" rest-api
