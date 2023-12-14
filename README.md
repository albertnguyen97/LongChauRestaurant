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

pip install pymysql

Then, edit the init.py file in your project origin dir(the same as settings.py)
add:
import pymysql
pymysql.install_as_MySQLdb()

pip install cryptography

social-auth-account
pip install social-auth-app-django
