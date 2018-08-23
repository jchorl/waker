UID=$(shell id -u)
GID=$(shell id -g)
IP=$(shell ip addr show | grep -E "inet ([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v ' lo' | head -1 | grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v 255)

serve:
	docker run -it --rm \
		-v $(PWD):/waker \
		-w /waker/server \
		-e PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native \
		-v /run/user/1000/pulse:/run/user/1000/pulse:ro \
		-p 5000:5000 \
		jchorl/waker \
		sh -c "GOOGLE_APPLICATION_CREDENTIALS=\$$(pwd)/service-account-key.json FLASK_ENV=development FLASK_APP=main.py flask run --host=0.0.0.0"

prod:
	docker run -it -d \
		-v $(PWD):/waker \
		-w /waker/server \
		-e PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native \
		-v /run/user/1000/pulse:/run/user/1000/pulse:ro \
		-p 5000:5000 \
		--restart always \
		jchorl/waker \
		sh -c "GOOGLE_APPLICATION_CREDENTIALS=\$$(pwd)/service-account-key.json FLASK_ENV=production FLASK_APP=main.py flask run --host=0.0.0.0"

auth-calendar:
	docker run -it --rm \
		-v $(PWD):/waker \
		-w /waker/server \
		-p 5000:5000 \
		python:3.7 \
		sh -c "pip install -r requirements.txt && python gcalendar.py --noauth_local_webserver"

img-build:
	docker build -t jchorl/waker .

prod-img-build:
	docker build -f Dockerfile.pi -t jchorl/waker .

app-img-build:
	docker build -t jchorl/waker-app app

app:
	docker container run --rm -it \
		-v $(PWD)/app:/usr/src/app \
		-w /usr/src/app \
		-u $(UID):$(GID) \
		--net=host \
		node \
		sh -c 'REACT_NATIVE_PACKAGER_HOSTNAME="$(IP)" npm start -- --reset-cache'

app-deploy:
	docker container run --rm -it \
		-v $(PWD)/app:/usr/src/app \
		-w /usr/src/app \
		-u $(UID):$(GID) \
		jchorl/waker-app

.PHONY: app
