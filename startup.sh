ssh pi@widget05-pi

source venvs/LocalFileSharing/bin/activate

cd projects/LocalFileSharing
export FLASK_APP=server
export FLASK_ENV=development
flask run --host=0.0.0.0