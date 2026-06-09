#!/usr/bin/env bash

# Installer les dépendances
uv pip install -r requirements.txt

# RASSEMBLER LES STATICS (Ajoutez cette ligne)
python manage.py collectstatic --noinput

# Appliquer les migrations
python manage.py migrate --noinput