#!/usr/bin/env bash

# 1. Supprimer l'ancien dossier pour repartir sur une base propre
rm -rf staticfiles/

# 2. Lancer le collectstatic en forçant le nettoyage des anciens fichiers
python manage.py collectstatic --noinput --clear

# 3. Appliquer les migrations
python manage.py migrate --noinput