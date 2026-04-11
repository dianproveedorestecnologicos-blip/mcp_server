# 🧠 MCP Inventario - Guía Completa (Python + MySQL + Claude Desktop)

Este proyecto implementa un **servidor MCP (Model Context Protocol)** en Python para gestionar un inventario, conectado a una base de datos MySQL (Laragon) y consumido desde **Claude Desktop**.

---

# 📌 Arquitectura

```
Claude Desktop
      ↓
MCP Server (Python)
      ↓
MySQL / MariaDB (Laragon)
```

---

# ⚙️ Requisitos

* Python 3.10 o superior
* Laragon (MySQL o MariaDB activo)
* Claude Desktop instalado
* Windows

---

# 📁 Estructura del proyecto

```
C:\laragon\www\mcp_server
│
├── server.py
├── db.py
├── requirements.txt
└── venv/
```

---

# 1️⃣ Crear el proyecto

```bash
cd C:\laragon\www
mkdir mcp_server
cd mcp_server
```

---

# 2️⃣ Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

---

# 3️⃣ Instalar dependencias

```bash
pip install mcp pydantic pymysql
```

Crear `requirements.txt`:

```txt
mcp
pydantic
pymysql
```

---

# 4️⃣ Configurar base de datos

```sql
CREATE DATABASE IF NOT EXISTS mcp_inventario
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE mcp_inventario;

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    sku VARCHAR(50) NOT NULL UNIQUE,
    stock INT NOT NULL DEFAULT 0,
    precio DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    categoria VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

# 5️⃣ Configurar conexión

Archivo `db.py`:

```python
import pymysql

def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="mcp_inventario",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
```

---

# 6️⃣ Ejecutar MCP

```bash
python server.py
```

✔ Si no hay errores → OK

---

# 7️⃣ Configurar Claude Desktop

Archivo:

```
%APPDATA%\Claude\claude_desktop_config.json
```

Contenido:

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

---

# 8️⃣ Probar

Ejemplos:

* Lista los productos
* Busca TEC-001
* Agrega un producto

---

# ⚠️ Problemas comunes

* Error rutas → validar paths
* Error MySQL → revisar Laragon
* MCP no aparece → reiniciar Claude

---

# 🚀 Mejoras futuras

* Movimientos de inventario
* Paginación
* .env
* Docker
* MCP remoto

---

# 🧾 Resumen

MCP = capa de negocio para IA.
