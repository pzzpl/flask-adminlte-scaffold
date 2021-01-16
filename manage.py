#!/usr/bin/env python3
import os
from app import create_app
from flask_script import Manager, Server

#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app('development')
manager = Manager(app)

server = Server(host="127.0.0.1", port=5000)
manager.add_command("runserver", server)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
