from gunicorn.app.base import BaseApplication
from main import app

import gunicorn.glogging
import gunicorn.workers.sync

class EncounterAPI(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    options = {
        'bind': ':8090',  # Change this to your desired host and port
        'workers': 3,  # Adjust the number of worker processes as needed
    }
    EncounterAPI(app, options).run()
