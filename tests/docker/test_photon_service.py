import requests
import os

# Haal de host op uit de docker-compose.yml, of gebruik localhost als standaard
PHOTON_HOST = os.environ.get("PHOTON_HOST", "photon")
PHOTON_PORT = 2322

def test_photon_api_is_healthy():
    """Controleert of de Photon service draait en een geldig antwoord geeft."""
    url = f"http://{PHOTON_HOST}:{PHOTON_PORT}/reverse?lon=5.1214&lat=52.0907"

    # 1. Maak de API-aanvraag
    response = requests.get(url)

    # 2. Controleer of de statuscode OK is (200)
    assert response.status_code == 200, "API gaf geen 200 OK status terug"

    # 3. Controleer of het antwoord geldig JSON is
    data = response.json()
    assert isinstance(data, dict), "Antwoord is geen geldig JSON-object"

    # 4. Controleer de structuur van het antwoord
    assert "features" in data, "JSON-antwoord mist de 'features' sleutel"
    assert len(data["features"]) > 0, "Geen locaties gevonden"

    properties = data["features"][0].get("properties", {})
    assert properties.get("country") == "Nederland", "Verwachte land niet gevonden"
    assert properties.get("city") == "Utrecht", "Verwachte stad niet gevonden"

    print("\nPhoton service test geslaagd!")