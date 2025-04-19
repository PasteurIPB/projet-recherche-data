#!/bin/bash
# Script pour exécuter l'intégration entre KoboToolbox et Dataverse

# Chemin d'accès au conteneur Python
CONTAINER_NAME="integration_python"

# Vérifier si le conteneur existe déjà, sinon le créer
if [ ! "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Création du conteneur d'intégration..."
    docker run -d --name $CONTAINER_NAME \
        --network research-data-network \
        -v "$(pwd)/scripts:/scripts" \
        python:3.9 \
        tail -f /dev/null
    
    # Installation des dépendances
    docker exec $CONTAINER_NAME pip install requests pandas
fi

# Exécution du script d'intégration
echo "Lancement du script d'intégration..."
docker exec $CONTAINER_NAME python /scripts/kobo_to_dataverse.py

echo "Intégration terminée."
