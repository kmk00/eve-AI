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
    
    def test_create_default_config_when_none_exists(self, config_service, mock_session):
        """Test creating default config when database is empty."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = None
        mock_session.exec.return_value = mock_result
        
        # Act
        result = config_service.load_from_db(mock_session)
        
        # Assert
        assert result is not None
        assert result.mode == "local"
        assert result.model_name == "gemma3:latest"
        assert result.gpu_layers == 60
        assert result.temperature == 0.7
        assert result.max_tokens == 4096
        assert result.conversation_memory_length == 10
        assert result.emotion_confidence_threshold == 0.6
        assert config_service._cache == result
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
    
    def test_cache_is_updated_after_load(self, config_service, mock_session, sample_config):
        """Test that cache is properly updated after loading."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = sample_config
        mock_session.exec.return_value = mock_result
        
        # Act
        assert config_service._cache is None
        config_service.load_from_db(mock_session)
        
        # Assert
        assert config_service._cache is not None
        assert config_service._cache == sample_config


class TestGetRuntimeConfig:
    """Tests for get_runtime_config method."""
    
    def test_get_config_from_cache(self, config_service, sample_config):
        """Test retrieving config from cache."""
        # Arrange
        config_service._cache = sample_config
        
        # Act
        result = config_service.get_runtime_config()
        
        # Assert
        assert result == sample_config
    
    def test_raise_error_when_cache_empty(self, config_service):
        """Test that RuntimeError is raised when cache is not loaded."""
        # Act & Assert
        with pytest.raises(RuntimeError, match="Config not loaded. Call load_from_db\\(\\) first."):
            config_service.get_runtime_config()


class TestUpdateRuntimeConfig:
    """Tests for update_runtime_config method."""
    
    def test_update_single_field(self, config_service, mock_session, sample_config):
        """Test updating a single config field."""
        # Arrange
        config_service._cache = sample_config
        
        # Act
        result = config_service.update_runtime_config(mock_session, temperature=0.9)
        
        # Assert
        assert result.temperature == 0.9
        mock_session.add.assert_called_once_with(sample_config)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_config)
    
    def test_update_multiple_fields(self, config_service, mock_session, sample_config):
        """Test updating multiple config fields."""
        # Arrange
        config_service._cache = sample_config
        
        # Act
        result = config_service.update_runtime_config(
            mock_session,
            temperature=0.8,
            max_tokens=2048,
            gpu_layers=40
        )
        
        # Assert
        assert result.temperature == 0.8
        assert result.max_tokens == 2048
        assert result.gpu_layers == 40
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
    
    def test_raise_error_when_cache_empty(self, config_service, mock_session):
        """Test that RuntimeError is raised when cache is not loaded."""
        # Act & Assert
        with pytest.raises(RuntimeError, match="Config not loaded. Call load_from_db\\(\\) first."):
            config_service.update_runtime_config(mock_session, temperature=0.9)
    
    def test_raise_error_for_invalid_field(self, config_service, mock_session, sample_config):
        """Test that ValueError is raised for invalid config fields."""
        # Arrange
        config_service._cache = sample_config
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid config field: invalid_field"):
            config_service.update_runtime_config(mock_session, invalid_field="value")
    
    def test_cache_is_updated_after_update(self, config_service, mock_session, sample_config):
        """Test that cache reflects the updated values."""
        # Arrange
        config_service._cache = sample_config
        original_temp = sample_config.temperature
        
        # Act
        config_service.update_runtime_config(mock_session, temperature=0.95)
        
        # Assert
        assert config_service._cache.temperature == 0.95
        assert config_service._cache.temperature != original_temp


class TestReloadFromDb:
    """Tests for reload_from_db method."""
    
    def test_reload_clears_cache_and_loads_fresh(self, config_service, mock_session, sample_config):
        """Test that reload clears cache and loads fresh data."""
        # Arrange
        old_config = Config(
            id=1,
            mode="cloud",
            model_name="old-model",
            gpu_layers=30,
            temperature=0.5,
            max_tokens=2048,
            conversation_memory_length=5,
            emotion_confidence_threshold=0.5
        )
        config_service._cache = old_config
        
        mock_result = Mock()
        mock_result.first.return_value = sample_config
        mock_session.exec.return_value = mock_result
        
        # Act
        result = config_service.reload_from_db(mock_session)
        
        # Assert
        assert result == sample_config
        assert config_service._cache == sample_config
        assert config_service._cache != old_config
    
    def test_reload_creates_default_if_none_exists(self, config_service, mock_session):
        """Test that reload creates default config if database is empty."""
        # Arrange
        config_service._cache = Mock()  # Some old cache
        
        mock_result = Mock()
        mock_result.first.return_value = None
        mock_session.exec.return_value = mock_result
        
        # Act
        result = config_service.reload_from_db(mock_session)
        
        # Assert
        assert result is not None
        assert result.mode == "local"
        assert config_service._cache == result
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()


class TestIntegration:
    """Integration tests for typical usage patterns."""
    
    def test_typical_workflow(self, config_service, mock_session, sample_config):
        """Test a typical workflow: load, get, update, reload."""
        # Load
        mock_result = Mock()
        mock_result.first.return_value = sample_config
        mock_session.exec.return_value = mock_result
        
        config_service.load_from_db(mock_session)
        
        # Get
        config = config_service.get_runtime_config()
        assert config == sample_config
        
        # Update
        updated = config_service.update_runtime_config(mock_session, temperature=0.85)
        assert updated.temperature == 0.85
        
        # Reload
        reloaded = config_service.reload_from_db(mock_session)
        assert reloaded == sample_config
    
    def test_cannot_update_before_load(self, config_service, mock_session):
        """Test that update fails if load was not called first."""
        with pytest.raises(RuntimeError):
            config_service.update_runtime_config(mock_session, temperature=0.9)
    
    def test_cannot_get_before_load(self, config_service):
        """Test that get fails if load was not called first."""
        with pytest.raises(RuntimeError):
            config_service.get_runtime_config()