from app.transform.normalizer import MetadataNormalizer

class MetadataTransformer:

    def transform_columns(self, raw_columns):
        """
        raw_columns es la lista que devuelve extractor.extract_columns()
        Formato esperado: [(column_name, data_type), ...]
        """
        transformed = []

        for col_name, col_type in raw_columns:
            transformed.append({
                "name": MetadataNormalizer.normalize_name(col_name),
                "type": MetadataNormalizer.normalize_type(col_type),
                "original_type": col_type
            })

        return transformed

    def transform_tables(self, raw_tables):
        """
        raw_tables es lista de nombres de tablas.
        """
        return [MetadataNormalizer.normalize_name(t) for t in raw_tables]
