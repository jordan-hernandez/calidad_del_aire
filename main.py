import requests

def get_page(date_from, date_to, api_key):
    response = requests.get(
        "https://api.openaq.org/v2/measurements",
        params={
            "city": "Cali",
            "date_from": date_from,
            "date_to": date_to,
            "limit": "10000",
            "order": "asc",
        },
        headers={
            "Authorization": f"Bearer {"54a8076ac004468de579c72682f37e15fbf6298e81105a0e6d54713ad4db4704"}"  # Usa tu clave de API aquí
        }
    )
    return response.json()

# Ejemplo de uso
api_key = "54a8076ac004468de579c72682f37e15fbf6298e81105a0e6d54713ad4db4704"
data = get_page("2023-01-01T00:00:00Z", "2023-01-31T23:59:59Z", api_key)
