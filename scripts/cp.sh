rsync -avz --delete --exclude=app --exclude=.git --exclude=server/__pycache__ --exclude=.config --exclude=server/output.mp3 . waker:waker/
