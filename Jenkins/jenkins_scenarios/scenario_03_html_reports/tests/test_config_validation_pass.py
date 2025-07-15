"""
Scenario 03: HTML Reports Chaos - Config Validation Tests (PASS)

These tests demonstrate proper configuration validation patterns
that should always pass in a well-configured environment.
"""

import pytest
import yaml
import json
import os
import tempfile
from pathlib import Path


class TestConfigValidationPass:
    """Test configuration validation scenarios that should pass"""

    def test_yaml_config_valid_structure(self):
        """Test that YAML configuration has valid structure and required fields"""
        config_data = {
            'app': {
                'name': 'chaos-workshop-app',
                'version': '1.0.0',
                'environment': 'test'
            },
            'database': {
                'host': 'localhost',
                'port': 5432,
                'name': 'testdb',
                'ssl_mode': 'require'
            },
            'cache': {
                'redis_url': 'redis://localhost:6379',
                'ttl': 3600
            },
            'logging': {
                'level': 'INFO',
                'format': 'json'
            }
        }
        
        # Create temporary YAML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f, default_flow_style=False)
            config_file = f.name
        
        try:
            # Validate YAML can be loaded
            with open(config_file, 'r') as f:
                loaded_config = yaml.safe_load(f)
            
            # Validate required sections exist
            assert 'app' in loaded_config, "App configuration section missing"
            assert 'database' in loaded_config, "Database configuration section missing"
            assert 'cache' in loaded_config, "Cache configuration section missing"
            assert 'logging' in loaded_config, "Logging configuration section missing"
            
            # Validate app section
            app_config = loaded_config['app']
            assert app_config['name'] == 'chaos-workshop-app', "App name mismatch"
            assert app_config['version'] == '1.0.0', "App version mismatch"
            assert app_config['environment'] in ['dev', 'test', 'staging', 'prod'], "Invalid environment"
            
            # Validate database section
            db_config = loaded_config['database']
            assert isinstance(db_config['port'], int), "Database port must be integer"
            assert 1 <= db_config['port'] <= 65535, "Database port out of valid range"
            assert db_config['ssl_mode'] in ['require', 'prefer', 'disable'], "Invalid SSL mode"
            
            # Validate cache section
            cache_config = loaded_config['cache']
            assert cache_config['redis_url'].startswith(('redis://', 'rediss://')), "Invalid Redis URL format"
            assert isinstance(cache_config['ttl'], int), "TTL must be integer"
            assert cache_config['ttl'] > 0, "TTL must be positive"
            
            # Validate logging section
            log_config = loaded_config['logging']
            assert log_config['level'] in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], "Invalid log level"
            assert log_config['format'] in ['json', 'text'], "Invalid log format"
            
        finally:
            # Clean up temporary file
            os.unlink(config_file)

    def test_environment_variables_present(self):
        """Test that required environment variables are properly set"""
        # Set test environment variables
        test_env_vars = {
            'APP_NAME': 'chaos-workshop-app',
            'APP_VERSION': '1.0.0',
            'DATABASE_URL': 'postgresql://user:pass@localhost:5432/testdb',
            'REDIS_URL': 'redis://localhost:6379',
            'LOG_LEVEL': 'INFO'
        }
        
        # Set environment variables for test
        for key, value in test_env_vars.items():
            os.environ[key] = value
        
        try:
            # Validate environment variables
            assert os.getenv('APP_NAME') == 'chaos-workshop-app', "APP_NAME not set correctly"
            assert os.getenv('APP_VERSION') == '1.0.0', "APP_VERSION not set correctly"
            assert os.getenv('DATABASE_URL').startswith('postgresql://'), "Invalid DATABASE_URL format"
            assert os.getenv('REDIS_URL').startswith('redis://'), "Invalid REDIS_URL format"
            assert os.getenv('LOG_LEVEL') in ['DEBUG', 'INFO', 'WARNING', 'ERROR'], "Invalid LOG_LEVEL"
            
            # Test database URL parsing
            db_url = os.getenv('DATABASE_URL')
            assert 'localhost' in db_url, "Database host not found in URL"
            assert '5432' in db_url, "Database port not found in URL"
            assert 'testdb' in db_url, "Database name not found in URL"
            
        finally:
            # Clean up environment variables
            for key in test_env_vars.keys():
                os.environ.pop(key, None)

    def test_json_config_schema_validation(self):
        """Test that JSON configuration follows the expected schema"""
        config_schema = {
            "type": "object",
            "required": ["service", "ports", "health_check"],
            "properties": {
                "service": {
                    "type": "object",
                    "required": ["name", "version"],
                    "properties": {
                        "name": {"type": "string", "minLength": 1},
                        "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"}
                    }
                },
                "ports": {
                    "type": "object",
                    "required": ["http", "health"],
                    "properties": {
                        "http": {"type": "integer", "minimum": 1, "maximum": 65535},
                        "health": {"type": "integer", "minimum": 1, "maximum": 65535}
                    }
                },
                "health_check": {
                    "type": "object",
                    "required": ["path", "interval"],
                    "properties": {
                        "path": {"type": "string"},
                        "interval": {"type": "integer", "minimum": 1}
                    }
                }
            }
        }
        
        valid_config = {
            "service": {
                "name": "chaos-workshop-service",
                "version": "1.0.0"
            },
            "ports": {
                "http": 8080,
                "health": 8081
            },
            "health_check": {
                "path": "/health",
                "interval": 30
            }
        }
        
        # Create temporary JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(valid_config, f, indent=2)
            config_file = f.name
        
        try:
            # Load and validate JSON
            with open(config_file, 'r') as f:
                loaded_config = json.load(f)
            
            # Basic structure validation
            assert isinstance(loaded_config, dict), "Config must be a dictionary"
            assert 'service' in loaded_config, "Service section missing"
            assert 'ports' in loaded_config, "Ports section missing"
            assert 'health_check' in loaded_config, "Health check section missing"
            
            # Service validation
            service = loaded_config['service']
            assert service['name'] == 'chaos-workshop-service', "Service name mismatch"
            assert service['version'] == '1.0.0', "Service version mismatch"
            
            # Ports validation
            ports = loaded_config['ports']
            assert isinstance(ports['http'], int), "HTTP port must be integer"
            assert isinstance(ports['health'], int), "Health port must be integer"
            assert 1 <= ports['http'] <= 65535, "HTTP port out of range"
            assert 1 <= ports['health'] <= 65535, "Health port out of range"
            assert ports['http'] != ports['health'], "HTTP and health ports must be different"
            
            # Health check validation
            health = loaded_config['health_check']
            assert health['path'].startswith('/'), "Health check path must start with /"
            assert isinstance(health['interval'], int), "Health check interval must be integer"
            assert health['interval'] > 0, "Health check interval must be positive"
            
        finally:
            # Clean up temporary file
            os.unlink(config_file)

    def test_configuration_file_permissions(self):
        """Test that configuration files have appropriate permissions"""
        # Create test configuration file
        config_content = """
app:
  name: chaos-workshop-app
  secret_key: not-a-real-secret
database:
  password: not-a-real-password
        """.strip()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(config_content)
            config_file = f.name
        
        try:
            # Set appropriate permissions (owner read/write only)
            os.chmod(config_file, 0o600)
            
            # Check file permissions
            file_stat = os.stat(config_file)
            file_mode = file_stat.st_mode & 0o777
            
            # Validate permissions are restrictive
            assert file_mode == 0o600, f"Config file permissions too permissive: {oct(file_mode)}"
            
            # Validate file is readable by owner
            assert os.access(config_file, os.R_OK), "Config file not readable by owner"
            
            # Validate file content can be loaded
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
            
            assert config_data['app']['name'] == 'chaos-workshop-app', "Config content validation failed"
            
        finally:
            # Clean up temporary file
            os.unlink(config_file)

    def test_config_validation_with_defaults(self):
        """Test configuration validation with default values"""
        def get_config_value(key: str, default=None, required: bool = False):
            """Helper function to get configuration values with defaults"""
            value = os.getenv(key, default)
            if required and value is None:
                raise ValueError(f"Required configuration key '{key}' not found")
            return value
        
        # Set some environment variables
        os.environ['APP_NAME'] = 'chaos-workshop'
        os.environ['APP_DEBUG'] = 'false'
        
        try:
            # Test required configuration
            app_name = get_config_value('APP_NAME', required=True)
            assert app_name == 'chaos-workshop', "Required config value incorrect"
            
            # Test optional configuration with defaults
            app_port = int(get_config_value('APP_PORT', '8080'))
            assert app_port == 8080, "Default port value incorrect"
            
            app_debug = get_config_value('APP_DEBUG', 'false').lower() == 'true'
            assert app_debug is False, "Debug flag should be False"
            
            log_level = get_config_value('LOG_LEVEL', 'INFO')
            assert log_level == 'INFO', "Default log level incorrect"
            
            # Test database URL with defaults
            db_host = get_config_value('DB_HOST', 'localhost')
            db_port = int(get_config_value('DB_PORT', '5432'))
            db_name = get_config_value('DB_NAME', 'chaos_workshop')
            
            assert db_host == 'localhost', "Default DB host incorrect"
            assert db_port == 5432, "Default DB port incorrect"
            assert db_name == 'chaos_workshop', "Default DB name incorrect"
            
            # Construct database URL
            db_url = f"postgresql://{db_host}:{db_port}/{db_name}"
            assert 'postgresql://localhost:5432/chaos_workshop' == db_url, "Constructed DB URL incorrect"
            
        finally:
            # Clean up environment variables
            os.environ.pop('APP_NAME', None)
            os.environ.pop('APP_DEBUG', None)

    def test_config_interpolation_and_references(self):
        """Test configuration with variable interpolation and references"""
        # Set base environment variables
        test_env = {
            'BASE_URL': 'https://api.example.com',
            'API_VERSION': 'v1',
            'SERVICE_NAME': 'chaos-workshop',
            'ENVIRONMENT': 'test'
        }
        
        for key, value in test_env.items():
            os.environ[key] = value
        
        try:
            # Test configuration interpolation
            base_url = os.getenv('BASE_URL')
            api_version = os.getenv('API_VERSION')
            service_name = os.getenv('SERVICE_NAME')
            environment = os.getenv('ENVIRONMENT')
            
            # Construct derived configuration values
            api_endpoint = f"{base_url}/{api_version}"
            service_endpoint = f"{api_endpoint}/services/{service_name}"
            health_endpoint = f"{service_endpoint}/health"
            
            # Validate interpolated values
            assert api_endpoint == 'https://api.example.com/v1', "API endpoint interpolation failed"
            assert service_endpoint == 'https://api.example.com/v1/services/chaos-workshop', "Service endpoint interpolation failed"
            assert health_endpoint == 'https://api.example.com/v1/services/chaos-workshop/health', "Health endpoint interpolation failed"
            
            # Test environment-specific configuration
            log_level = 'DEBUG' if environment == 'dev' else 'INFO'
            assert log_level == 'INFO', "Environment-specific log level incorrect"
            
            debug_mode = environment in ['dev', 'test']
            assert debug_mode is True, "Debug mode should be enabled for test environment"
            
            # Test configuration validation
            assert base_url.startswith('https://'), "Base URL must use HTTPS"
            assert api_version.startswith('v'), "API version must start with 'v'"
            assert len(service_name) > 0, "Service name cannot be empty"
            assert environment in ['dev', 'test', 'staging', 'prod'], "Invalid environment"
            
        finally:
            # Clean up environment variables
            for key in test_env.keys():
                os.environ.pop(key, None)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])