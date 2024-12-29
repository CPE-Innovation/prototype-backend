from flask import Blueprint, request, jsonify
from prototype.services.ProjectService import ProjectService

project_bp = Blueprint('project', __name__)

@project_bp.route('/projects')
def get_projects():
    return

@project_bp.route('/project/<int:project_id>', methods=['GET'])
def get_project(project_id):
    return

@project_bp.route('/project/risks/<int:project_id>', methods=['GET'])
def get_risks(project_id):
    return # All risks associated with a project

@project_bp.route('/project', methods=['POST'])
def add_project():
    data = request.json
    return ProjectService.addProject(data.get("name"))
