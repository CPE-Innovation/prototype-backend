from flask import Blueprint, request, jsonify
from prototype.services.modelService import ModelService

model_bp = Blueprint('model', __name__, url_prefix='/model')

@model_bp.route('/fetch', methods=['GET'])
def fetch():
    # Dans le service associé (modelController ): 
    # - Utiliser script de Raph pour fetch depuis son JSON (service.preprocessing)
    # - Utiliser mon script pour process (service.processing)
    # - Mettre à jour la DB (risk et projects)
    print("Received fetch request.")
    ModelService.fetch_data()
    return

