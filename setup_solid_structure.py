#!/usr/bin/env python
import os
import sys

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Creado directorio: {path}")

def create_file(path, content=""):
    with open(path, 'w') as f:
        f.write(content)
    print(f"Creado archivo: {path}")

def create_init_file(path):
    init_path = os.path.join(path, "__init__.py")
    if not os.path.exists(init_path):
        create_file(init_path)

def setup_solid_structure(app_name):
    base_dir = app_name
    
    # Verificar que la app existe
    if not os.path.exists(base_dir):
        print(f"Error: La aplicación '{app_name}' no existe.")
        return
    
    # Estructura principal
    directories = [
        "models",
        "services",
        "repositories",
        "views",
        "serializers",
        "interfaces",
        "factories",
        "utils",
        "tests/unit",
        "tests/integration",
        "forms",
        "templates/{0}".format(app_name),
        "static/{0}/css".format(app_name),
        "static/{0}/js".format(app_name),
        "static/{0}/img".format(app_name),
    ]
    
    # Crear directorios y archivos __init__.py
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        create_directory(dir_path)
        create_init_file(dir_path)
        
        # Para los directorios principales, crear archivos base
        if directory in ["models", "services", "repositories", "views", "serializers", "interfaces"]:
            base_file = os.path.join(dir_path, f"base_{directory[:-1]}.py")
            create_file(base_file, f"# Base {directory[:-1]} para implementar principios SOLID\n")
    
    # Crear archivos específicos con plantillas básicas
    create_file(
        os.path.join(base_dir, "repositories", "base_repository.py"),
        "from abc import ABC, abstractmethod\n\n"
        "class BaseRepository(ABC):\n"
        "    \"\"\"Interface for repository pattern following Dependency Inversion Principle\"\"\"\n"
        "    \n"
        "    @abstractmethod\n"
        "    def get_all(self):\n"
        "        pass\n"
        "    \n"
        "    @abstractmethod\n"
        "    def get_by_id(self, id):\n"
        "        pass\n"
        "    \n"
        "    @abstractmethod\n"
        "    def create(self, entity):\n"
        "        pass\n"
        "    \n"
        "    @abstractmethod\n"
        "    def update(self, entity):\n"
        "        pass\n"
        "    \n"
        "    @abstractmethod\n"
        "    def delete(self, id):\n"
        "        pass\n"
    )
    
    create_file(
        os.path.join(base_dir, "services", "base_service.py"),
        "class BaseService:\n"
        "    \"\"\"Base service class following Single Responsibility Principle\"\"\"\n"
        "    \n"
        "    def __init__(self, repository):\n"
        "        \"\"\"Dependency Injection of repository\"\"\"\n"
        "        self.repository = repository\n"
    )
    
    create_file(
        os.path.join(base_dir, "interfaces", "base_interface.py"),
        "from abc import ABC, abstractmethod\n\n"
        "class BaseInterface(ABC):\n"
        "    \"\"\"Base interface following Interface Segregation Principle\"\"\"\n"
        "    pass\n"
    )
    
    # Modificar el archivo apps.py para registrar la app correctamente
    apps_content = (
        "from django.apps import AppConfig\n\n\n"
        f"class {app_name.capitalize()}Config(AppConfig):\n"
        "    default_auto_field = 'django.db.models.BigAutoField'\n"
        f"    name = '{app_name}'\n"
        "\n"
        "    def ready(self):\n"
        "        # Import señales o configuraciones necesarias al iniciar la app\n"
        "        pass\n"
    )
    create_file(os.path.join(base_dir, "apps.py"), apps_content)
    
    # Crear archivo README.md con instrucciones
    readme_content = (
        f"# {app_name.capitalize()} Django App\n\n"
        "Esta aplicación sigue los principios SOLID y patrones de diseño:\n\n"
        "- **S (Responsabilidad Única)**: Cada clase tiene una única responsabilidad\n"
        "- **O (Abierto/Cerrado)**: Las clases están abiertas para extensión, cerradas para modificación\n"
        "- **L (Sustitución de Liskov)**: Las subclases pueden sustituir a sus clases base\n"
        "- **I (Segregación de Interfaces)**: Interfaces específicas mejor que una general\n"
        "- **D (Inversión de Dependencias)**: Dependemos de abstracciones, no implementaciones\n\n"
        "## Estructura del proyecto\n\n"
        "- **models/**: Modelos de datos y entidades\n"
        "- **repositories/**: Implementación del patrón Repository para acceso a datos\n"
        "- **services/**: Lógica de negocio\n"
        "- **interfaces/**: Interfaces y contratos\n"
        "- **views/**: Controladores y vistas de Django\n"
        "- **serializers/**: Serializadores para API Rest\n"
        "- **factories/**: Implementación del patrón Factory\n"
        "- **utils/**: Utilidades y helpers\n"
        "- **tests/**: Pruebas unitarias e integración\n"
    )
    create_file(os.path.join(base_dir, "README.md"), readme_content)
    
    print(f"\nEstructura SOLID creada exitosamente para la app '{app_name}'")
    print(f"Consulta el archivo README.md en la carpeta {app_name} para más información.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python setup_solid_structure.py nombre_app")
        sys.exit(1)
    
    app_name = sys.argv[1]
    setup_solid_structure(app_name)