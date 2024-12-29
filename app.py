from flask import Flask
from prototype.extensions import db, migrate
from prototype.config import Config
from prototype.controller.projectController import project_bp
from prototype.controller.modelController import model_bp

def create_app(config_class=Config):
    app = Flask(__name__) 
    app.config.from_object(config_class)
    app.register_blueprint(project_bp)
    app.register_blueprint(model_bp)

    db.init_app(app)
    migrate.init_app(app)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__" :
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port="5000", debug=True)