# MCP Inventario - Guia de uso (Python + MySQL + Claude Desktop)

Servidor MCP en Python para administrar inventario en MySQL/MariaDB.

## Arquitectura

```text
Claude Desktop
      ->
MCP Server (Python)
      ->
MySQL / MariaDB (Laragon)
```

## Requisitos

- Python 3.10+
- Laragon con MySQL/MariaDB activo
- Claude Desktop
- Windows (esta guia usa rutas Windows)

## Estructura del proyecto

```text
C:\laragon\www\mcp_server
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
```

## 1) Crear y activar entorno virtual

```powershell
cd C:\laragon\www\mcp_server
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 2) Instalar dependencias

```powershell
pip install -r requirements.txt
```

Dependencias actuales:

- mcp
- pydantic
- pymysql
- python-dotenv

## 3) Configurar base de datos

Ejecuta el SQL de `db/query.txt` en MySQL.

## 4) Configurar variables de entorno

Crea un `.env` local a partir de `.env.example`:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=mcp_inventario
```

Notas:

- `DB_USER` y `DB_NAME` son obligatorias.
- `DB_PORT` debe ser un numero entero valido.
- `.env` esta ignorado por Git.

## 5) Ejecutar servidor MCP

```powershell
python server.py
```

## 6) Configurar Claude Desktop

Archivo:

```text
%APPDATA%\Claude\claude_desktop_config.json
```

Ejemplo:

```json
{
  "mcpServers": {
    "inventario-python": {
      "command": "C:\\laragon\\www\\mcp_server\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\laragon\\www\\mcp_server\\server.py"
      ]
    }
  }
}
```

## Herramientas MCP disponibles

- `listar_productos(limit=20)`
- `buscar_producto(texto)`
- `obtener_producto_por_id(id_producto)`
- `agregar_producto(producto)`
- `actualizar_stock(id_producto, nuevo_stock)`
- `eliminar_producto(id_producto)`

## Buenas practicas aplicadas

- Credenciales fuera del codigo fuente (`.env`).
- Validacion de variables de entorno obligatorias en conexion de DB.
- Uso de `Decimal` para precios en lugar de `float`.
- Validacion para evitar busquedas vacias.
- `.gitignore` con patrones basicos de Python.

## Problemas comunes

- No conecta a MySQL: validar variables en `.env`.
- Error de puerto: revisar `DB_PORT`.
- Claude no ve el servidor: reiniciar Claude Desktop y revisar rutas.
