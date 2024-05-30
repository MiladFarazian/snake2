import logging

from flask import Flask, render_template
from gunicorn.app.base import BaseApplication

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def root_route():
    return render_template("index.html")


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


# Do not remove the main function while updating the app.
if __name__ == "__main__":
    options = {"bind": "%s:%s" % ("0.0.0.0", "8080"), "workers": 4, "loglevel": "info"}
    StandaloneApplication(app, options).run()
