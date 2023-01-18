# API REST Train Filtering
# Tester en local
/!\ Bien mettre le booléen "docker" à False dans le fichier \_\_init__.py /!\

![DockerOn](./imgReadMe/docker%20off.png)

## Comment lancer le Flask
### Créer un venv et l'activer
> .../webservice> python -m venv .venv
#### Pour Windows (par CMD) :
> .../webservice> cd .venv/Scripts
> .../webservice/.venv/Scripts> activate.bat
#### Pour Linux :
> .../webservice> ./.venv/Scripts/activate

### Installer les bibliothèques python
> .../webservice/.venv/Scripts> cd ../..
> .../webservice> python.exe -m pip install --upgrade pip
> .../webservice> pip install -r requirements.txt

### Lancer l'app flask
> .../webservice> [python -m flask|flask] --app '.\REST Train Filtering\FlaskApp\app\\\_\_init__.py' run

si cela ne fonctionne pas, deplacer vous dans .\REST Train Filtering\FlaskApp\app et réaliser la commande :
> .../webservice/REST Train Filtering/FlaskApp/app> [python -m flask|flask] --app \_\_init__.py run

#### Flask disponible
> http://127.0.0.1:5000

### Lancer la base de donnée
#### Télécharger le logiciel
> [**XAMPP**](https://www.apachefriends.org/fr/download.html) (si cela n'est pas déjà fait)

Ensuite lancer les serveurs Apache et MySQL :
![Launch serveurs](./imgReadMe/StartServ.png)

Rendez-vous dans le phpMyAdmin en cliquant sur le bouton :
![ReachAdmin](./imgReadMe/GoToAdmin.png)

ou par ce lien :
> http://localhost/phpmyadmin/

Créer une nouvelle base de données:
![CreateDB](./imgReadMe/CreateNewDB.png)

Nommez la "secf" et appuyez sur "Créer":
![CreateDBname](./imgReadMe/CreateNewDBname.png)
Et importez le fichier *secf.sql*
> ...\webservice\\"REST Train Filtering"\secf.sql

![Import](./imgReadMe/import.png)

# Tester via Docker

/!\ Bien mettre le booléen "docker" à True dans le fichier \_\_init__.py /!\

![DockerOn](./imgReadMe/docker%20on.png)

### Lancer Docker
#### Télécharger le logiciel
> [**Docker**](https://www.docker.com/products/docker-desktop/) (si cela n'est pas déjà fait)

#### Créer le docker
> docker-compose up --build

#### Flask disponible 
> http://localhost:8888

#### phpMyAdmin disponible
> user et mot de passe : root 
> http://localhost:8088

# Tester les requêtes :
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/21869921-4f5bffde-fe57-45e0-aae8-93a8e9ee8f10?action=collection%2Ffork&collection-url=entityId%3D21869921-4f5bffde-fe57-45e0-aae8-93a8e9ee8f10%26entityType%3Dcollection%26workspaceId%3Db4f7b72c-3ff2-4187-ac64-0b43944985ca)

# API SOAP Train booking
# Tester
Pro Tips: utiliser 2 terminaux pour lancer le serveur et le client

## Préparation du SOAP
> .../webservice> cd SOAP
### Créer un venv et l'activer
> .../webservice/SOAP> python -m venv .venv
#### Pour Windows (par CMD) :
> .../webservice/SOAP> cd .venv/Scripts
> .../webservice/SOAP/.venv/Scripts> activate.bat
#### Pour Linux :
> .../webservice/SOAP> ./.venv/Scripts/activate

### Installer les bibliothèques python
> .../webservice/SOAP/.venv/Scripts> cd ../..
> .../webservice/SOAP> python.exe -m pip install --upgrade pip
> .../webservice/SOAP> pip install -r requirements.txt
## Lancer le serveur
> .../webservice/SOAP> [py|python|python3] server.py

## Lancer le client
> .../webservice/SOAP> [py|python|python3] client.py