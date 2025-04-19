#!/bin/bash
# Script pour d�marrer l'ensemble de la plateforme

echo "D�marrage de la plateforme de donn�es de recherche..."

# 1. Cr�er les r�pertoires n�cessaires si besoin
mkdir -p traefik

# 2. D�marrer les services de base (PostgreSQL et Traefik)
echo "D�marrage des services de base..."
docker-compose up -d

# 3. D�marrer KoboToolbox
echo "D�marrage de KoboToolbox..."
docker-compose -f docker-compose.kobo.yml up -d

# 4. D�marrer Dataverse
echo "D�marrage de Dataverse..."
docker-compose -f docker-compose.dataverse.yml up -d

# 5. D�marrer Apache Superset
echo "D�marrage d'Apache Superset..."
docker-compose -f docker-compose.superset.yml up -d

echo "La plateforme est en cours de d�marrage. Veuillez patienter quelques minutes..."
echo "Vous pourrez ensuite acc�der aux services via les URLs suivants:"
echo "- KoboToolbox: http://kobo.localhost"
echo "- Dataverse: http://dataverse.localhost"
echo "- Apache Superset: http://superset.localhost"