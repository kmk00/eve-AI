import pytest
from unittest.mock import Mock, MagicMock
from sqlmodel import Session
from app.services.config_service import ConfigService
from app.models.schemas import Config

@pytest.fixture
def mock_session():
    """Create a mock database session."""
    return Mock(spec=Session)

@pytest.fixture
def config_service():
    """Create a fresh ConfigService instance for each test."""
    return ConfigService()


@pytest.fixture
def sample_config():
    """Create a sample config object."""
    return Config(
        id=1,
        mode="local",
        model_name="gemma3:latest",
        gpu_layers=60,
        temperature=0.7,
        max_tokens=4096,
        conversation_memory_length=10,
        emotion_confidence_threshold=0.6
    )
    


class TestLoadFromDb:
    """Tests for load_from_db method."""
    
    def test_load_existing_config(self, config_service, mock_session, sample_config):
        """Test loading existing config from database."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = sample_config
        mock_session.exec.return_value = mock_result
        
        # Act
        result = config_service.load_from_db(mock_session)
        
        # Assert
        assert result == sample_config
        assert config_service._cache == sample_config
        mock_session.exec.assert_called_once()
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()