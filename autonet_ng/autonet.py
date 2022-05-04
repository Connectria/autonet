import argparse
import logging

from db import init_db
from wsgi import run_wsgi_app
from commands.createadmin import create_admin

parser = argparse.ArgumentParser()
parser.add_argument('command', default='run')
args, _ = parser.parse_known_args()

LOG = logging.getLogger()

LOG.info("Application started via CLI.")
if args.command == 'createadmin':
    init_db()
    create_admin()
if args.command == 'run':
    run_wsgi_app()
