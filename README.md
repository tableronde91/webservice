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
> .../webservice> flask --app app run
###### ou
> .../webservice> python -m flask --app app run

##### Aller sur un navigateur
> http://127.0.0.1:5000