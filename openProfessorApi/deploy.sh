if [ ! -d /usr/share/nginx/html/gunicorn/open_professor ];
then
    mkdir -p /usr/share/nginx/html/gunicorn/open_professor
fi
cp -r * /usr/share/nginx/html/gunicorn/open_professor/
cd /usr/share/nginx/html/gunicorn/open_professor

if [ ! -d /usr/share/nginx/html/gunicorn/open_professor/venv ];
then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
chown -R nginx:nginx /usr/share/nginx/html/gunicorn/open_professor
