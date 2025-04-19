#!/usr/bin/env python3
"""
Script d'intégration pour transférer automatiquement les données 
de KoboToolbox vers Dataverse.
"""
import requests
import json
import os
import pandas as pd
from datetime import datetime

# Configuration
KOBO_URL = "http://kpi:8000"
KOBO_USERNAME = "admin"
KOBO_PASSWORD = "admin"  # À remplacer par votre mot de passe réel
DATAVERSE_URL = "http://dataverse:8080"
DATAVERSE_API_KEY = "votre-cle-api"  # À générer et remplacer

def get_kobo_token():
    """Obtient un token d'authentification pour l'API KoboToolbox"""
    response = requests.post(
        f"{KOBO_URL}/api/v2/token/",
        data={
            "username": KOBO_USERNAME,
            "password": KOBO_PASSWORD
        }
    )
    
    if response.status_code == 200:
        return response.json().get("token")
    else:
        raise Exception(f"Échec d'authentification: {response.text}")

def get_kobo_forms(token):
    """Récupère la liste des formulaires disponibles"""
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(
        f"{KOBO_URL}/api/v2/assets/?format=json",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        raise Exception(f"Échec de récupération des formulaires: {response.text}")

def get_kobo_data(token, asset_uid):
    """Récupère les données d'un formulaire spécifique"""
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(
        f"{KOBO_URL}/api/v2/assets/{asset_uid}/data/?format=json",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        raise Exception(f"Échec de récupération des données: {response.text}")

def send_to_dataverse(data, form_name, form_id):
    """Envoie les données à Dataverse"""
    headers = {"X-Dataverse-key": DATAVERSE_API_KEY}
    
    # Conversion en DataFrame pour faciliter l'exportation en CSV
    df = pd.DataFrame(data)
    
    # Préparation des métadonnées au format Dataverse
    metadata = {
        "datasetVersion": {
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "title",
                            "value": f"Données {form_name} - {datetime.now().strftime('%Y-%m-%d')}"
                        },
                        {
                            "typeName": "author",
                            "value": [{"authorName": {"value": "Import Automatique KoboToolbox"}}]
                        },
                        {
                            "typeName": "datasetContact",
                            "value": [{"datasetContactEmail": {"value": "admin@example.com"}}]
                        },
                        {
                            "typeName": "dsDescription",
                            "value": [{"dsDescriptionValue": {"value": f"Données collectées via le formulaire {form_name} (ID: {form_id})"}}]
                        },
                        {
                            "typeName": "subject",
                            "value": ["Research Data"]
                        }
                    ]
                }
            }
        }
    }
    
    # Création du dataset dans Dataverse
    response = requests.post(
        f"{DATAVERSE_URL}/api/dataverses/root/datasets",
        headers=headers,
        json=metadata
    )
    
    if response.status_code == 201:
        dataset_id = response.json()["data"]["id"]
        
        # Sauvegarde temporaire des données en CSV
        csv_path = f"/tmp/{form_id}.csv"
        df.to_csv(csv_path, index=False)
        
        # Ajout du fichier CSV au dataset
        with open(csv_path, 'rb') as f:
            files = {'file': (f"{form_id}.csv", f)}
            file_response = requests.post(
                f"{DATAVERSE_URL}/api/datasets/{dataset_id}/add",
                headers=headers,
                files=files
            )
        
        # Suppression du fichier temporaire
        os.remove(csv_path)
        
        if file_response.status_code == 200:
            # Publication du dataset
            publish_response = requests.post(
                f"{DATAVERSE_URL}/api/datasets/{dataset_id}/actions/:publish",
                headers=headers,
                params={"type": "major"}
            )
            return publish_response.status_code == 200
    
    return False

def main():
    """Fonction principale qui orchestre le transfert de données"""
    print("Démarrage du transfert KoboToolbox → Dataverse...")
    
    try:
        # Authentification
        token = get_kobo_token()
        print("Authentification réussie.")
        
        # Récupération des formulaires
        forms = get_kobo_forms(token)
        print(f"Nombre de formulaires trouvés: {len(forms)}")
        
        for form in forms:
            form_id = form.get("uid")
            form_name = form.get("name")
            
            print(f"Traitement du formulaire: {form_name} (ID: {form_id})...")
            
            # Récupération des données du formulaire
            data = get_kobo_data(token, form_id)
            print(f"  - {len(data)} entrées récupérées.")
            
            if data:
                # Envoi à Dataverse
                success = send_to_dataverse(data, form_name, form_id)
                if success:
                    print(f"  - Données importées avec succès dans Dataverse.")
                else:
                    print(f"  - Échec de l'importation dans Dataverse.")
            else:
                print("  - Aucune donnée à importer.")
        
        print("Transfert terminé.")
    
    except Exception as e:
        print(f"Erreur lors du transfert: {str(e)}")

if __name__ == "__main__":
    main()

