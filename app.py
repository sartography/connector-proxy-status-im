import os
from flask import Flask
from spiff_connector.spiff_connector_blueprint import spiff_connector_blueprint

app = Flask(__name__)

app.config.from_pyfile("config.py", silent=True)

if app.config["ENV"] != "production":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Use the SpiffConnector Blueprint, which will auto-discover any
# connector-* packages and provide API endpoints for listing and executing
# available services.
app.register_blueprint(spiff_connector_blueprint)

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
