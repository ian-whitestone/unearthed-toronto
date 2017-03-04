import os
import sys

from flask_script import Manager, Server
from web import app

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0',
    port = '12345'
))

if __name__ == "__main__":
    manager.run()
