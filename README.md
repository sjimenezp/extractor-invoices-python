# Invoice XML Extractor

Extractor de facturas XML mexicanas (formato SAT/CFDI 4.0) que convierte la información en formato tabular para facilitar su uso en hojas de cálculo.

## Descripción

Esta aplicación procesa archivos XML de facturas electrónicas del SAT (México) y extrae la información relevante:
- UUID (primeros 8 caracteres)
- Fecha de emisión
- RFC del emisor
- Nombre del emisor
- Tipo de gasto (basado en el nombre de la carpeta)
- Total de la factura

Los datos se muestran en una tabla en la terminal y se copian automáticamente al portapapeles para pegarlos directamente en Excel.

## Requisitos

- Python 3.8+
- Dependencias (ver `pyproject.toml`):
  - `pyperclip` - Para copiar al portapapeles
  - `tabulate` - Para mostrar tablas en terminal

## Instalación

```bash
# Usando uv (recomendado)
uv sync

# O usando pip
pip install -e .
```

## Uso

```bash
# Ejecutar con uv (recomendado)
uv run app.py

# O ejecutar con Python directamente
python app.py
```

### Primera ejecución

1. Al ejecutar por primera vez, el programa te pedirá el directorio donde están tus facturas XML
2. Este directorio se guardará en `config.ini` para futuras ejecuciones
3. Si presionas Enter sin escribir nada, usará el directorio actual

### Estructura de directorios

El programa organiza las facturas por tipo de gasto basándose en la estructura de carpetas:

```
facturas/
├── Gasolina/
│   ├── factura1.xml
│   └── factura2.xml
├── Oficina/
│   ├── factura3.xml
│   └── factura4.xml
└── factura5.xml  (se clasificará como "Gasolina" por defecto)
```

## Características

- Procesa múltiples archivos XML recursivamente
- Ordena automáticamente por fecha y tipo de gasto
- Copia los datos al portapapeles en formato compatible con Excel
- Maneja errores de archivos XML corruptos o malformados
- Guarda el directorio de trabajo para uso futuro

## Configuración

El archivo `config.ini` se crea automáticamente la primera vez que ejecutas el programa. Para cambiar el directorio de trabajo, simplemente ingresa una nueva ruta cuando el programa lo solicite.

## Autor

Copyright © 2024
GitHub: [@sjimenezp](https://github.com/sjimenezp)
