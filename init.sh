mkdir -p project/log
mkdir -p project/report
mkdir -p project/test_automation
mkdir -p project/tmp
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser