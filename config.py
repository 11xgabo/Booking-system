import os
from pydantic_settings import BaseSettings, SettingsConfigForm

class Settings(BaseSettings):
    # Pydantic leerá automáticamente estas variables desde el archivo .env
    supabase_url: str
    supabase_key: str

    # Configuración para que apunte al archivo .env
    model_config = SettingsConfigForm(env_file=".env", env_file_encoding="utf-8")

# Instanciamos la configuración para poder importarla
settings = Settings()

# Mantenemos las variables con los nombres que usaste en tu main.py
SUPABASE_URL = settings.supabase_url
SUPABASE_KEY = settings.supabase_key