IMAGE_NAME=playwright-auto-select-cert

# Chrome
build-and-run-chrome:
	docker build -t $(IMAGE_NAME) -f "./Dockerfile-chrome" .
	docker run -it $(IMAGE_NAME)

# Firefox
build-and-run-firefox:
	docker build -t $(IMAGE_NAME) -f "./Dockerfile-firefox" .
	docker run -it $(IMAGE_NAME)