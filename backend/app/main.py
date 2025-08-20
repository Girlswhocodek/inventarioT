from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import sqlite3
import json

app = FastAPI(title="CMDB Inventory API")

class ConfigurationItem(BaseModel):
    id: int = None
    name: str
    type: str
    attributes: dict = {}

# Base de datos temporal (luego cambiamos a PostgreSQL)
DB_PATH = "/tmp/cmdb.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuration_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            attributes TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.get("/")
async def root():
    return {"message": "✅ CMDB Inventory API Running!", "status": "active"}

@app.get("/items", response_model=List[ConfigurationItem])
async def get_all_items():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM configuration_items")
    items = cursor.fetchall()
    conn.close()
    
    return [
        ConfigurationItem(
            id=item[0],
            name=item[1],
            type=item[2],
            attributes=json.loads(item[3]) if item[3] else {}
        ) for item in items
    ]

@app.post("/items", response_model=ConfigurationItem)
async def create_item(item: ConfigurationItem):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO configuration_items (name, type, attributes) VALUES (?, ?, ?)",
        (item.name, item.type, json.dumps(item.attributes))
    )
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    
    return {**item.dict(), "id": item_id}

# Inicializar base de datos al startup
init_db()
