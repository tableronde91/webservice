# Comment lancer le Flask
### Créer un venv et l'activer
> .../webservice> python -m venv .venv
##### Pour Windows (par CMD) :
> .../webservice> cd .venv/Scripts
> .../webservice/.venv/Scripts> activate.bat
##### Pour Linux :
> .../webservice> ./.venv/Scripts/activate

### Installer les bibliothèques python
> .../webservice/.venv/Scripts> cd ../..
> .../webservice> python.exe -m pip install --upgrade pip
> .../webservice> pip install -r requirements.txt

### Lancer l'app flask
> .../webservice> flask --app '.\REST Train Filtering\FlaskApp\app\__init__.py' run
###### ou
> .../webservice> python -m flask --app '.\REST Train Filtering\FlaskApp\app\__init__.py' run

##### Aller sur un navigateur
> http://127.0.0.1:5000


##### Tester les requêtes :
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/21869921-4f5bffde-fe57-45e0-aae8-93a8e9ee8f10?action=collection%2Ffork&collection-url=entityId%3D21869921-4f5bffde-fe57-45e0-aae8-93a8e9ee8f10%26entityType%3Dcollection%26workspaceId%3Db4f7b72c-3ff2-4187-ac64-0b43944985ca)