# shortcut for rebuilding the database
# only for development/debugging purposes

echo "Fresh random secret key"
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

Remove-Item -Recurse .\cmb\cmb_home\migrations
Remove-Item -Recurse .\cmb\cmb_contact\migrations
Remove-Item .\cmb\db.sqlite3

.\dvenv\Scripts\Activate.ps1
python .\cmb\manage.py makemigrations cmb_home
python .\cmb\manage.py makemigrations cmb_contact
python .\cmb\manage.py migrate
python .\cmb\manage.py hmock
python .\cmb\manage.py createadmin
python .\cmb\manage.py runsslserver localhost:443