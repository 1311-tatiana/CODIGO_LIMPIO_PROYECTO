"""Configuracion central de la API."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Valores de configuracion leidos desde variables de entorno."""

    app_name: str = "Inventario Ferreteria API"
    app_version: str = "1.0.0"
    database_path: Path = Path("src/storage/database.json")
    supabase_url: str | None = os.getenv("SUPABASE_URL")
    supabase_key: str | None = os.getenv("SUPABASE_KEY")
    supabase_table_productos: str = os.getenv("SUPABASE_TABLE_PRODUCTOS", "productos")
    use_supabase: bool = os.getenv("USE_SUPABASE", "false").lower() == "true"

    @property
    def supabase_configured(self) -> bool:
        """Indica si existen credenciales minimas para usar Supabase."""

        return bool(self.supabase_url and self.supabase_key)


settings = Settings()
