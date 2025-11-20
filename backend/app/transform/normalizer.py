# app/transform/normalizer.py

class MetadataNormalizer:
    """
    Normaliza tipos de datos y nombres para unificar el catálogo.
    """

    GENERIC_TYPES = {
        # TEXTOS
        "varchar": "STRING",
        "varchar2": "STRING",
        "nvarchar": "STRING",
        "char": "STRING",
        "nchar": "STRING",
        "text": "STRING",
        "clob": "STRING",

        # NUMÉRICOS
        "int": "INTEGER",
        "integer": "INTEGER",
        "smallint": "INTEGER",
        "bigint": "INTEGER",
        "number": "INTEGER",
        "decimal": "DECIMAL",
        "numeric": "DECIMAL",
        "float": "FLOAT",
        "double": "FLOAT",
        "real": "FLOAT",

        # FECHAS
        "date": "DATE",
        "datetime": "DATETIME",
        "timestamp": "DATETIME",
    }

    @classmethod
    def normalize_type(cls, db_type: str):
        if not db_type:
            return "UNKNOWN"

        db_type = db_type.lower().strip()

        return cls.GENERIC_TYPES.get(db_type, "UNKNOWN")

    @classmethod
    def normalize_name(cls, name: str):
        return name.strip().lower()
