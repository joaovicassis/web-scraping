import pytest
from fastapi.testclient import TestClient
from api import app
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Cria cliente de teste
client = TestClient(app)

def test_root_endpoint():
    """Testa o endpoint raiz."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data

def test_health_check():
    """Testa o endpoint de saúde."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data

def test_search_endpoint_basic():
    """Testa o endpoint de busca com parâmetros básicos."""
    response = client.get("/search?query=teste")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_search_endpoint_with_filters():
    """Testa o endpoint de busca com filtros."""
    response = client.get("/search?query=teste&uf=SP&modalidade=OPERADORA")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_search_endpoint_pagination():
    """Testa o endpoint de busca com paginação."""
    response = client.get("/search?query=teste&limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5

def test_search_endpoint_invalid_params():
    """Testa o endpoint de busca com parâmetros inválidos."""
    response = client.get("/search?query=")  # query vazia
    assert response.status_code == 422

def test_search_endpoint_invalid_limit():
    """Testa o endpoint de busca com limit inválido."""
    response = client.get("/search?query=teste&limit=-1")
    assert response.status_code == 422

def test_search_endpoint_invalid_offset():
    """Testa o endpoint de busca com offset inválido."""
    response = client.get("/search?query=teste&offset=-1")
    assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__]) 