IMAGE_NAME=playwright-auto-select-cert

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -it $(IMAGE_NAME)