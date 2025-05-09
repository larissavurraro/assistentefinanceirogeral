import os

def dump_env_json_to_file(env_var_name, filename):
    """
    Recebe o nome da variável de ambiente (ex: 'GOOGLE_CLOUD_CREDENTIALS')
    e salva o conteúdo dela em /tmp/<filename>. Retorna o path para o arquivo.
    """
    path = f"/tmp/{filename}"
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(os.environ[env_var_name])
    return path
