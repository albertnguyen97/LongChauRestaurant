Cat dat csdl
sudo apt update
sudo apt install mysql-server -y
sudo mysql_secure_installation
sudo mysql -u root -p
CREATE USER 'bigcat'@'localhost' IDENTIFIED BY 'yourpassword';
CREATE DATABASE restaurant;
GRANT ALL PRIVILEGES ON djangodb.* TO 'admindjango1'@'localhost';
FLUSH PRIVILEGES;
EXIT;
pip install pymysql
# giong voi config database trong settings
pip install pymysql

Then, edit the init.py file in your project origin dir(the same as settings.py)
add:
import pymysql
pymysql.install_as_MySQLdb()

pip install cryptography

social-auth-account
pip install social-auth-app-django

python -m pip install celery==5.4.0


docker pull rabbitmq:3.13.1-management
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13.1-management
celery chaulong worker -l info
docker run -it --rm --name redis -p 6379:6379 redis:7.2.4

# cai dat thu vien bo xung

pip install celery python-decouple

pip install django-import-export
pip install django-ckeditor-5
pip install django-rosetta
pip install django-extensions
pip install redis
pip install stripe
pip install weasyprint
pip install django-bleach
pip install tinycss2
pip install django-summernote

# cat dat stripe
stripe cli


