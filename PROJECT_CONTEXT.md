# Contexto del Proyecto: mcp_server

Ultima actualizacion: 2026-04-11
Objetivo: contexto persistente para acelerar futuras tareas en este repo.

## Estructura actual (sin __pycache__)

```text
mcp_server/
|- .env
|- .env.example
|- .gitignore
|- PROJECT_CONTEXT.md
|- Readme.md
|- db.py
|- requirements.txt
|- server.py
|- data/
|  |- inventario.json
|- db/
|  |- query.txt
|- venv/
|  |- ... (entorno virtual)
```

## Funcion del proyecto

Servidor MCP en Python para administrar inventario sobre MySQL/MariaDB.

Flujo:
1. Cliente MCP (ej. Claude Desktop) invoca tools en `server.py`.
2. `server.py` opera SQL usando `get_connection()` de `db.py`.
3. `db.py` toma configuracion de `.env`.
4. Se trabaja sobre `mcp_inventario.productos`.

## Archivos clave

- `server.py`
  - Modelos: `Producto`, `ProductoInput`
  - Tools: listar, buscar, obtener por id, agregar, actualizar stock, eliminar
  - Buenas practicas: `precio` en `Decimal`, rechazo de busqueda vacia

- `db.py`
  - Carga `.env` con `python-dotenv`
  - Valida variables obligatorias: `DB_USER`, `DB_NAME`
  - Valida `DB_PORT` como entero
  - Conexion en `utf8mb4`

- `db/query.txt`
  - Script SQL para crear DB/tabla y datos semilla

- `.env.example`
  - Plantilla publica de variables de entorno

- `Readme.md`
  - Guia de instalacion, configuracion y ejecucion alineada al codigo actual

## Configuracion esperada (.env)

Variables usadas:
- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

## Dependencias

- mcp
- pydantic
- pymysql
- python-dotenv

## Comandos utiles

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python server.py
```

## Nota de mantenimiento

Si cambia codigo o configuracion, actualizar tambien este archivo y `Readme.md` para evitar desalineacion.
