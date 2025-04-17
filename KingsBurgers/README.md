# Kingsburgers Django App

Esta aplicación sigue los principios SOLID y patrones de diseño:

- **S (Responsabilidad Única)**: Cada clase tiene una única responsabilidad
- **O (Abierto/Cerrado)**: Las clases están abiertas para extensión, cerradas para modificación
- **L (Sustitución de Liskov)**: Las subclases pueden sustituir a sus clases base
- **I (Segregación de Interfaces)**: Interfaces específicas mejor que una general
- **D (Inversión de Dependencias)**: Dependemos de abstracciones, no implementaciones

## Estructura del proyecto

- **models/**: Modelos de datos y entidades
- **repositories/**: Implementación del patrón Repository para acceso a datos
- **services/**: Lógica de negocio
- **interfaces/**: Interfaces y contratos
- **views/**: Controladores y vistas de Django
- **serializers/**: Serializadores para API Rest
- **factories/**: Implementación del patrón Factory
- **utils/**: Utilidades y helpers
- **tests/**: Pruebas unitarias e integración
