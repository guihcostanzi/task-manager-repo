import json
import os

def get_db_url():
    # Caminho para o arquivo de configuração
    cfg_path = os.path.join('config', 'supabase_cfg.json')
    with open(cfg_path, 'r') as f:
        config = json.load(f)
    return config.get('SUPABASE_DB_URL')