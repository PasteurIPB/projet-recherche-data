#!/bin/bash
# Script pour ex�cuter l'int�gration entre KoboToolbox et Dataverse

# Chemin d'acc�s au conteneur Python
CONTAINER_NAME="integration_python"

# V�rifier si le conteneur existe d�j�, sinon le cr�er
if [ ! "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Cr�ation du conteneur d'int�gration..."
    docker run -d --name $CONTAINER_NAME \
        --network research-data-network \
        -v "$(pwd)/scripts:/scripts" \
        python:3.9 \
        tail -f /dev/null
    
    # Installation des d�pendances
    docker exec $CONTAINER_NAME pip install requests pandas
fi

# Ex�cution du script d'int�gration
echo "Lancement du script d'int�gration..."
docker exec $CONTAINER_NAME python /scripts/kobo_to_dataverse.py

echo "Int�gration termin�e."
