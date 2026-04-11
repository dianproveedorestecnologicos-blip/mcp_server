from __future__ import annotations

from typing import Optional, List
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP
from db import get_connection

mcp = FastMCP(
    name="Inventario MCP",
    instructions=(
        "Servidor MCP para administrar inventario en MySQL. "
        "Permite listar, buscar, agregar, actualizar stock y eliminar productos.",
    ),
)

class Producto(BaseModel):
    id: int
    nombre: str = Field(..., min_length=1)
    sku: str = Field(..., min_length=1)
    stock: int = Field(..., ge=0)
    precio: float = Field(..., ge=0)
    categoria: str = Field(..., min_length=1)

class ProductoInput(BaseModel):
    nombre: str = Field(..., min_length=1)
    sku: str = Field(..., min_length=1)
    stock: int = Field(..., ge=0)
    precio: float = Field(..., ge=0)
    categoria: str = Field(..., min_length=1)

@mcp.tool()
def listar_productos(limit: int = 20) -> List[Producto]:
    """Lista productos del inventario."""
    limit = max(1, min(limit, 100))

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, nombre, sku, stock, precio, categoria
                FROM productos
                ORDER BY id ASC
                LIMIT %s
            """, (limit,))
            rows = cursor.fetchall()
            return [Producto(**row) for row in rows]
    finally:
        conn.close()

@mcp.tool()
def buscar_producto(texto: str) -> List[Producto]:
    """Busca productos por nombre o SKU."""
    texto = texto.strip()
    criterio = f"%{texto}%"

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, nombre, sku, stock, precio, categoria
                FROM productos
                WHERE nombre LIKE %s OR sku LIKE %s
                ORDER BY nombre ASC
                LIMIT 50
            """, (criterio, criterio))
            rows = cursor.fetchall()
            return [Producto(**row) for row in rows]
    finally:
        conn.close()

@mcp.tool()
def obtener_producto_por_id(id_producto: int) -> Optional[Producto]:
    """Obtiene un producto por id."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, nombre, sku, stock, precio, categoria
                FROM productos
                WHERE id = %s
            """, (id_producto,))
            row = cursor.fetchone()
            return Producto(**row) if row else None
    finally:
        conn.close()

@mcp.tool()
def agregar_producto(producto: ProductoInput) -> Producto:
    """Agrega un producto nuevo validando que el SKU no exista."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id
                FROM productos
                WHERE LOWER(sku) = LOWER(%s)
            """, (producto.sku.strip(),))
            existe = cursor.fetchone()

            if existe:
                raise ValueError(f"Ya existe un producto con el SKU '{producto.sku}'.")

            cursor.execute("""
                INSERT INTO productos (nombre, sku, stock, precio, categoria)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                producto.nombre.strip(),
                producto.sku.strip(),
                producto.stock,
                producto.precio,
                producto.categoria.strip(),
            ))

            nuevo_id = cursor.lastrowid

            cursor.execute("""
                SELECT id, nombre, sku, stock, precio, categoria
                FROM productos
                WHERE id = %s
            """, (nuevo_id,))
            row = cursor.fetchone()

            return Producto(**row)
    finally:
        conn.close()

@mcp.tool()
def actualizar_stock(id_producto: int, nuevo_stock: int) -> Producto:
    """Actualiza el stock de un producto."""
    if nuevo_stock < 0:
        raise ValueError("El stock no puede ser negativo.")

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE productos
                SET stock = %s
                WHERE id = %s
            """, (nuevo_stock, id_producto))

            if cursor.rowcount == 0:
                raise ValueError(f"No existe un producto con id {id_producto}.")

            cursor.execute("""
                SELECT id, nombre, sku, stock, precio, categoria
                FROM productos
                WHERE id = %s
            """, (id_producto,))
            row = cursor.fetchone()

            return Producto(**row)
    finally:
        conn.close()

@mcp.tool()
def eliminar_producto(id_producto: int) -> dict:
    """Elimina un producto por id."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, nombre, sku, stock, precio, categoria
                FROM productos
                WHERE id = %s
            """, (id_producto,))
            row = cursor.fetchone()

            if not row:
                raise ValueError(f"No existe un producto con id {id_producto}.")

            cursor.execute("""
                DELETE FROM productos
                WHERE id = %s
            """, (id_producto,))

            return {
                "ok": True,
                "mensaje": "Producto eliminado correctamente.",
                "producto": row,
            }
    finally:
        conn.close()

if __name__ == "__main__":
    mcp.run()