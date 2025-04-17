# Kingsburgers Django App

Esta aplicaci�n sigue los principios SOLID y patrones de dise�o:

- **S (Responsabilidad �nica)**: Cada clase tiene una �nica responsabilidad
- **O (Abierto/Cerrado)**: Las clases est�n abiertas para extensi�n, cerradas para modificaci�n
- **L (Sustituci�n de Liskov)**: Las subclases pueden sustituir a sus clases base
- **I (Segregaci�n de Interfaces)**: Interfaces espec�ficas mejor que una general
- **D (Inversi�n de Dependencias)**: Dependemos de abstracciones, no implementaciones

## Estructura del proyecto

- **models/**: Modelos de datos y entidades
- **repositories/**: Implementaci�n del patr�n Repository para acceso a datos
- **services/**: L�gica de negocio
- **interfaces/**: Interfaces y contratos
- **views/**: Controladores y vistas de Django
- **serializers/**: Serializadores para API Rest
- **factories/**: Implementaci�n del patr�n Factory
- **utils/**: Utilidades y helpers
- **tests/**: Pruebas unitarias e integraci�n
