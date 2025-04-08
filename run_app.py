from flask.cli import load_dotenv
import os
from flaskr import create_app


load_dotenv()
if __name__ == '__main__':
    app = create_app()
    app.run(debug=os.getenv('FLASK_DEBUG'), host=os.getenv('ADRESSE_SRV_FLASK'), port=os.getenv('FLASK_RUN_PORT'))