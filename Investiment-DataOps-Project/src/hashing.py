import hashlib

def calculate_hash(*args):
    """
    Calcula um hash SHA-256 para os argumentos dados.

    Args:
        *args: os valores a serem incluídos no hash.

    Returns:
        str: o hash dos valores.
    """
    # Combina os argumentos em uma única string
    key = ''.join(str(arg) for arg in args)

    # Calcula o hash da chave
    hash_object = hashlib.sha256(key.encode())
    hex_dig = hash_object.hexdigest()

    return hex_dig
