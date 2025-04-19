#!/bin/bash
# Script pour arrêter tous les services de la plateforme

echo "Arrêt de la plateforme de données de recherche..."

# 1. Arrêter Apache Superset
echo "Arrêt d'Apache Superset..."
docker-compose -f docker-compose.superset.yml down

# 2. Arrêter Dataverse
echo "Arrêt de Dataverse..."
docker-compose -f docker-compose.dataverse.yml down

# 3. Arrêter KoboToolbox
echo "Arrêt de KoboToolbox..."
docker-compose -f docker-compose.kobo.yml down

# 4. Arrêter les services de base
echo "Arrêt des services de base..."
docker-compose down

echo "Tous les services ont été arrêtés."