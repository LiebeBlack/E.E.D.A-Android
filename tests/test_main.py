import pytest
from src.core.database import DatabaseManager
from src.core.theme import DesignTokens

def test_database_initialization():
    db = DatabaseManager(":memory:")
    assert db.db_path == ":memory:", "La base de datos debería estar en memoria"
    
def test_design_tokens():
    colors = DesignTokens.COLORS
    assert "primary" in colors, "El tema debe rener el color primario"
    assert "bg_dark" in colors, "El tema debe rener el fondo bg_dark"

def test_protocol_color_alpha():
    color = DesignTokens.get_protocol_color("alpha")
    assert color == DesignTokens.COLORS["primary"]
