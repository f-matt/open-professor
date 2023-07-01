if [ ! -d /var/gunicorn/open_professor ];
then
    mkdir -p /var/gunicorn/open_professor
fi
cp -r * /var/gunicorn/open_professor/
cd /var/gunicorn/open_professor

if [ ! -d /var/gunicorn/open_professor/venv ];
then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
chown -R gunicorn:gunicorn /var/gunicorn/open_professor
