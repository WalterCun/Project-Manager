# Estructuras de Proyecto

Esta carpeta contiene las plantillas de estructura de proyecto en formato JSON. Estas plantillas definen la organización completa de carpetas y archivos para diferentes tipos de proyectos.

## Formato de las Plantillas

Cada archivo JSON de estructura debe tener el siguiente formato:

```json
{
  "name": "Nombre de la Estructura",
  "description": "Descripción detallada de la estructura",
  "version": "1.0",
  "author": "Autor de la plantilla",
  "structure": {
    "CARPETA_PRINCIPAL": {
      "Subcarpeta 1": {},
      "Subcarpeta 2": {
        "Archivo1.docx": "Descripción del archivo",
        "Archivo2.xlsx": "Descripción del archivo"
      },
      "Archivo Principal.txt": "Descripción del archivo principal"
    }
  }
}
```

## Estructuras Disponibles

### Default Business Structure
- **Archivo**: `default_business_structure.json`
- **Propósito**: Estructura completa para empresas de servicios turísticos
- **Características**:
  - 10 carpetas principales organizadas numéricamente
  - Subcarpetas especializadas por área
  - Archivos específicos con descripciones detalladas

## Uso

Las estructuras se cargan automáticamente por el sistema cuando se crea un proyecto. El usuario puede seleccionar diferentes estructuras según sus necesidades específicas.

## Creación de Nuevas Estructuras

Para crear una nueva estructura:

1. Crear un archivo JSON en esta carpeta
2. Seguir el formato establecido
3. Incluir metadata completa (name, description, version, author)
4. Definir la estructura jerárquica en el campo "structure"
5. Probar la estructura creando un proyecto de prueba

## Validación

El sistema valida automáticamente:
- Sintaxis JSON correcta
- Campos requeridos presentes
- Estructura jerárquica válida
- Nombres de archivos y carpetas permitidos