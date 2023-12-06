from apps.config import API_GENERATOR


def generate_forms_file():
    with open('api_generator/forms/forms_structure', 'r') as forms_structure_file:
        forms_structure = forms_structure_file.read()

    with open('api_generator/forms/library_imports', 'r') as library_imports_file:
        library_imports = library_imports_file.read()

    with open('api_generator/forms/base_imports', 'r') as base_imports_file:
        base_imports = base_imports_file.read()

    with open('api_generator/forms/base_form', 'r') as base_form_file:
        base_form = base_form_file.read()

    project_imports = base_imports.format(models_name=", ".join(API_GENERATOR.values()))
    forms = '\n\n'.join(base_form.format(model_name=model_name) for model_name in API_GENERATOR.values())
    generation = forms_structure.format(
        library_imports=library_imports,
        project_imports=project_imports,
        forms=forms
    )

    with open('apps/api/forms.py', 'w') as forms_py:
        forms_py.write(generation)

    return generation


def generate_routes_file():
    with open('api_generator/routes/routes_structure', 'r') as routes_structure_file:
        routes_structure = routes_structure_file.read()

    with open('api_generator/routes/library_imports', 'r') as library_imports_file:
        library_imports = library_imports_file.read()

    with open('api_generator/routes/base_imports', 'r') as base_imports_file:
        base_imports = base_imports_file.read()

    with open('api_generator/routes/base_route', 'r') as base_routes_file:
        base_routes = base_routes_file.read()
    project_imports = base_imports.format(
        models_name=', '.join(API_GENERATOR.values()),
        forms_name=', '.join(list(map(lambda model_name: f'{model_name}Form', API_GENERATOR.values())))
    )
    routes = '\n\n'.join(base_routes.format(
        form_name=f'{model_name}Form',
        model_name=model_name,
        endpoint=endpoint
    ) for endpoint, model_name in API_GENERATOR.items())

    generation = routes_structure.format(
        library_imports=library_imports,
        project_imports=project_imports,
        routes=routes
    )

    with open('apps/api/routes.py', 'w') as routes_py:
        routes_py.write(generation)

    return generation


if __name__ == '__main__':
    generate_routes_file()
    generate_forms_file()