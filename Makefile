serve:
	docker run -it --rm \
		-v $(PWD):/waker \
		-w /waker/server \
		-p 5000:5000 \
		python:3.7 \
		sh -c "pip install -r requirements.txt && GOOGLE_APPLICATION_CREDENTIALS=\$$(pwd)/service-account-key.json FLASK_ENV=development FLASK_APP=main.py flask run --host=0.0.0.0"

auth-calendar:
	docker run -it --rm \
		-v $(PWD):/waker \
		-w /waker/server \
		-p 5000:5000 \
		python:3.7 \
		sh -c "pip install -r requirements.txt && python gcalendar.py --noauth_local_webserver"
