# s4d_python
Beschrijving: Klein project voor S4D, supermarkt scraper

## Handleiding
De database docker container moet gestart zijn voor de flask container om connectie te maken. Mocht je de database ergens remote draaiende hebben, dan moet je in flask-production.py de "host=" aanpassen voor de database connectie variabele. Deze kun je op 127.0.0.1 zetten wanneer je beide containers lokaal draait.

Het bouwen van de docker images doe je met:
`sudo docker build -t <naam image> .` in de map van de database docker image (docker_images/database/) of de frontend docker image (docker_images/frontend/).

Het draaien van de docker containers doe je met:
`sudo docker run -d -p 3306:3306 <naam database image>` voor het runnen van de database container, en `sudo docker run -d -p 80:80 <naam frontend image>` voor het runnen van de frontend container.

Mocht je handmatig flask willen starten buiten docker om voor testdoeleinden, dan kun je dit doen door eerst het commando `export FLASK_APP=/root/flask-production.py` te draaien en daarna het commando `python3 -m flask run --host=0.0.0.0` te draaien. Op deze manier wordt de server lokaal gestart en is die beschikbaar voor het internet (mocht je dat niet willen haal je de `--host` tag weg.

Mocht je flask handmatig willen starten als productieomgeving, doe dit dan d.m.v. een productieserver als bijvoorbeeld `gunicorn`. Deze installeer je met `pip3 install gunicorn`. Vervolgens kun je de productieomgeving starten middels het commando `gunicorn --bind=0.0.0.0:80 flask-production:app`

De database is te vullen door de scraper te starten (main.py). Wanneer de database gevuld is en de flask server draait kun je deze benaderen door naar `127.0.0.1:80` te gaan.
