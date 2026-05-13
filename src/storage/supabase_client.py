"""Cliente de Supabase creado a partir de variables de entorno."""

from typing import Any

from src.core.config import settings


def get_supabase_client() -> Any:
    """Retorna un cliente de Supabase configurado.

    La importacion se hace dentro de la funcion para que la API pueda iniciar
    en modo local aunque el paquete supabase no este instalado todavia.
    """

    if not settings.supabase_configured:
        raise RuntimeError(
            "Faltan SUPABASE_URL y SUPABASE_KEY. Revisa tu archivo .env."
        )

    try:
        from supabase import create_client
    except ImportError as exc:
        raise RuntimeError(
            "Instala las dependencias con 'uv sync' antes de usar Supabase."
        ) from exc

    return create_client(settings.supabase_url, settings.supabase_key)
