from flask.cli import load_dotenv
import os
from flaskr import create_app


load_dotenv()
if __name__ == '__main__':
    app = create_app()
    # debug = os.getenv('FLASK_DEBUG', '0').lower() in ('1', 'true', 'yes')
    debug = os.getenv('FLASK_DEBUG', '1').lower() in ('1', 'true', 'yes')
    app.run(debug=debug, host=os.getenv('ADRESSE_SRV_FLASK'), port=os.getenv('FLASK_RUN_PORT'))