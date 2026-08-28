import os
os.environ.pop("DATABASE_URL", None)  # force le jeu de secours, pas de DB requise

from app import app

def test_sante():
    client = app.test_client()
    reponse = client.get("/sante")
    assert reponse.status_code == 200
    assert reponse.get_json()["statut"] == "operationnel"

def test_alertes_seuil():
    client = app.test_client()
    reponse = client.get("/alertes")
    assert reponse.status_code == 200
    donnees = reponse.get_json()
    assert all(s["velos_disponibles"] <= 0 for s in donnees["stations"])  # cassé exprès
