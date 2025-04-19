#!/bin/bash
# Script pour arr�ter tous les services de la plateforme

echo "Arr�t de la plateforme de donn�es de recherche..."

# 1. Arr�ter Apache Superset
echo "Arr�t d'Apache Superset..."
docker-compose -f docker-compose.superset.yml down

# 2. Arr�ter Dataverse
echo "Arr�t de Dataverse..."
docker-compose -f docker-compose.dataverse.yml down

# 3. Arr�ter KoboToolbox
echo "Arr�t de KoboToolbox..."
docker-compose -f docker-compose.kobo.yml down

# 4. Arr�ter les services de base
echo "Arr�t des services de base..."
docker-compose down

echo "Tous les services ont �t� arr�t�s."