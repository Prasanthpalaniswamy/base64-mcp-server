import base64

def encode_credentials(login: str, password: str) -> str:
    credentials = f"{login}:{password}"
    return base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

def decode_credentials(encoded_data: str) -> dict:
    decoded_bytes = base64.b64decode(encoded_data)
    decoded_string = decoded_bytes.decode("utf-8")

    if ":" not in decoded_string:
        raise ValueError("Invalid encoded credentials format")

    login, password = decoded_string.split(":", 1)

    return {
        "result": {
            "login": login,
            "password": password
        }
    }