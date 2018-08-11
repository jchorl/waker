serve:
	docker run -it --rm \
		-v $(PWD):/waker \
		-w /waker/server \
		-p 5000:5000 \
		python:3.7 \
		sh -c "pip install -r requirements.txt && FLASK_APP=main.py flask run --host=0.0.0.0"
