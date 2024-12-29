import requests
from datetime import datetime
import copy
import csv
from prototype.services.model_steps.IPreprocessing import IPreprocessing
#from IPreprocessing import IPreprocessing

class Preprocessing_APITest(IPreprocessing): 

    # Split between fetch and preprocess... Maybe preprocess is standardized and only fetch methods are implemented in different subclassess

    @staticmethod
    def preprocess(api_url="http://localhost:3000/messages", params=None):
        """
        Filtre les messages d'une API à partir d'une date et d'un ID utilisateur (facultatif),
        puis exporte les messages pertinents dans un fichier CSV.

        Args:
            api_url (str): L'URL de l'API à interroger.
            parmas (tuple) : 
                [0] : user_id (str, optional): L'ID de l'utilisateur pour filtrer les messages. Par défaut : None.
                [1] : ate_str (str, optional): La date (au format ISO 8601 : "YYYY-MM-DDTHH:MM:SSZ") pour filtrer les messages. Par défaut : None.
            output_csv (str): Le chemin du fichier CSV de sortie. Par défaut : "csv_messages.csv".
        """
        user_id = None; date_str = None
        if params:
            user_id, date_str = params

        # Configurer les paramètres de requête
        query_params = {}
        if user_id:
            query_params["from.user.id"] = user_id

        # Récupérer les messages de l'API
        response = requests.get(api_url, params=query_params)
        if response.status_code == 200:
            messages = response.json()
        else:
            print(f"Failed to fetch data from {api_url}. Status code: {response.status_code}")
            return

        # Convertir la date en objet datetime si fournie
        if date_str:
            try:
                timestamp_filter = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError as e:
                print(f"Erreur de format de date : {e}")
                return
        else:
            timestamp_filter = None

        # Filtrer les messages par date
        filtered_messages = []
        for msg in messages:
            try:
                msg_timestamp = datetime.strptime(msg["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
                if not timestamp_filter or msg_timestamp >= timestamp_filter:
                    filtered_messages.append(msg)
            except Exception as e:
                print(f"Erreur lors du traitement du message : {msg}")
                print(e)

        # Diviser les messages en phrases
        split_messages = []
        for message in filtered_messages:
            content = message.get("body", {}).get("content", "")
            sentences = [sentence.strip() for sentence in content.split(".") if sentence.strip()]
            for sentence in sentences:
                new_message = copy.deepcopy(message)
                new_message["body"]["content"] = sentence
                split_messages.append(new_message)

        # Préparer les données pour le CSV
        csv_messages = [
            {
                "PROJECT": msg.get("channel", "Unknown"),
                "MESSAGE": msg.get("body", {}).get("content", ""),
                "ORIGIN": "Teams",
                "DATE": datetime.strptime(msg.get("timestamp"), "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y")
            }
            for msg in split_messages
        ]

        return csv_messages

        # Écrire les messages dans un fichier CSV
        # try:
        #     with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        #         fieldnames = ["PROJECT", "MESSAGE", "ORIGIN", "DATE"]
        #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #         writer.writeheader()
        #         writer.writerows(csv_messages)

        #     print(f"Messages pertinents exportés dans '{output_csv}'")
        # except Exception as e:
        #     print(f"Erreur lors de l'écriture du fichier CSV : {e}")

    # # Exemple d'utilisation
    # filter_and_export_messages(
    #     api_url="http://localhost:3000/messages",
    #     user_id=None,  # Pas de filtre sur l'utilisateur
    #     date_str="2024-11-26T00:45:56Z"
    # )

if __name__ == "__main__":
    print("Fetching messages...")
    messages = Preprocessing_APITest.preprocess()
    print(messages)
