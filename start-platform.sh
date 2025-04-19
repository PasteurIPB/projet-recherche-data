#!/bin/bash
# Script pour démarrer l'ensemble de la plateforme

echo "Démarrage de la plateforme de données de recherche..."

# 1. Créer les répertoires nécessaires si besoin
mkdir -p traefik

# 2. Démarrer les services de base (PostgreSQL et Traefik)
echo "Démarrage des services de base..."
docker-compose up -d

# 3. Démarrer KoboToolbox
echo "Démarrage de KoboToolbox..."
docker-compose -f docker-compose.kobo.yml up -d

# 4. Démarrer Dataverse
echo "Démarrage de Dataverse..."
docker-compose -f docker-compose.dataverse.yml up -d

# 5. Démarrer Apache Superset
echo "Démarrage d'Apache Superset..."
docker-compose -f docker-compose.superset.yml up -d

echo "La plateforme est en cours de démarrage. Veuillez patienter quelques minutes..."
echo "Vous pourrez ensuite accéder aux services via les URLs suivants:"
echo "- KoboToolbox: http://kobo.localhost"
echo "- Dataverse: http://dataverse.localhost"
echo "- Apache Superset: http://superset.localhost"