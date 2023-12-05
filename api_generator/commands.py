import importlib

import click
import api_generator.manager as manager
from flask.cli import with_appcontext
from apps.config import API_GENERATOR


@click.command(name="gen_api")
@with_appcontext
def gen_api():
    for model in API_GENERATOR.values():
        try:
            models = importlib.import_module("apps.models")
            ModelClass = getattr(models, model)
            ModelClass.query.all()
        except Exception as e:
            print(f"Generation API failed because: {str(e)}")
            return

    try:
        manager.generate_forms_file()
        manager.generate_routes_file()
        print("APIs have been generated successfully.")
    except Exception as e:
        print(f"Generation API failed because: {str(e)}")
