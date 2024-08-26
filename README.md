# Description
- Django Rest Framework를 사용한 백엔드 애플리케이션입니다.
- `SECRET_KEY`를 위한 `DJANGO_SECRET_KEY`를 `.env`에 추가해주세요


# How to start server
```
echo 'DJANGO_SECRET_KEY="your_secret_key"' >> .env
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

# Requirements
```
asgiref==3.8.1
Django==5.1
django-dotenv==1.4.2
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
PyJWT==2.9.0
sqlparse==0.5.1
```
