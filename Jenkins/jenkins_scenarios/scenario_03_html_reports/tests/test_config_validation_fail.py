"""
Scenario 03: HTML Reports Chaos - Config Validation Tests (FAIL)

These tests simulate real-world configuration failures that should
always fail to demonstrate common enterprise configuration problems.
"""

import pytest
import yaml
import json
import os
import tempfile
from pathlib import Path


class TestConfigValidationFail:
    """Test configuration validation scenarios that should fail"""

    def test_yaml_config_malformed_syntax(self):
        """Test that malformed YAML configuration fails validation"""
        # Create malformed YAML content
        malformed_yaml = """
app:
  name: chaos-workshop-app
  version: 1.0.0
database:
  host: localhost
  port: 5432
  - invalid_list_syntax
cache:
  redis_url: redis://localhost:6379
  ttl: [unclosed_bracket
logging:
  level: INFO
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_file = f.name
        
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            # Check for circular dependencies
            def check_circular_deps(service_name, visited=None, path=None):
                if visited is None:
                    visited = set()
                if path is None:
                    path = []
                
                if service_name in visited:
                    return True  # Circular dependency found
                
                if service_name not in config:
                    return False
                
                visited.add(service_name)
                path.append(service_name)
                
                depends_on = config[service_name].get('depends_on', [])
                for dependency in depends_on:
                    if check_circular_deps(dependency, visited.copy(), path.copy()):
                        return True
                
                return False
            
            # This should detect circular dependencies and fail
            has_circular_deps = any(check_circular_deps(service) for service in config.keys())
            assert not has_circular_deps, "Circular dependencies detected in service configuration"
            
        finally:
            os.unlink(config_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])', suffix='.yaml', delete=False) as f:
            f.write(malformed_yaml)
            config_file = f.name
        
        try:
            # This should fail due to malformed YAML
            with open(config_file, 'r') as f:
                yaml.safe_load(f)
            
            # If we reach here, the test should fail
            pytest.fail("Expected YAML parsing to fail due to malformed syntax")
            
        except yaml.YAMLError:
            # This is expected - malformed YAML should fail
            pytest.fail("YAML parsing failed as expected, but this test is designed to always fail")
        finally:
            os.unlink(config_file)

    def test_missing_required_environment_variables(self):
        """Test failure when required environment variables are missing"""
        # Clear potentially existing environment variables
        required_vars = ['APP_NAME', 'DATABASE_URL', 'SECRET_KEY', 'API_TOKEN']
        original_values = {}
        
        for var in required_vars:
            original_values[var] = os.environ.pop(var, None)
        
        try:
            # Check for required environment variables that are now missing
            missing_vars = []
            for var in required_vars:
                if not os.getenv(var):
                    missing_vars.append(var)
            
            # This should always fail because we intentionally removed the vars
            assert len(missing_vars) == 0, f"Missing required environment variables: {missing_vars}"
            
            # Additional checks that will fail
            app_name = os.getenv('APP_NAME')
            assert app_name is not None, "APP_NAME environment variable is required"
            assert len(app_name) > 0, "APP_NAME cannot be empty"
            
            database_url = os.getenv('DATABASE_URL')
            assert database_url is not None, "DATABASE_URL environment variable is required"
            assert database_url.startswith('postgresql://'), "DATABASE_URL must be a valid PostgreSQL URL"
            
            secret_key = os.getenv('SECRET_KEY')
            assert secret_key is not None, "SECRET_KEY environment variable is required"
            assert len(secret_key) >= 32, "SECRET_KEY must be at least 32 characters"
            
        finally:
            # Restore original environment variables
            for var, value in original_values.items():
                if value is not None:
                    os.environ[var] = value

    def test_invalid_database_configuration(self):
        """Test failure with invalid database configuration"""
        config_data = {
            'database': {
                'host': '',  # Empty host - invalid
                'port': 999999,  # Port out of range
                'name': '',  # Empty database name
                'username': 'admin',
                'password': '123',  # Weak password
                'ssl_mode': 'invalid_mode',  # Invalid SSL mode
                'max_connections': -5,  # Negative connections
                'timeout': 0  # Zero timeout
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_file = f.name
        
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            db_config = config['database']
            
            # These validations should fail
            assert len(db_config['host'].strip()) > 0, "Database host cannot be empty"
            assert 1 <= db_config['port'] <= 65535, f"Database port {db_config['port']} out of valid range"
            assert len(db_config['name'].strip()) > 0, "Database name cannot be empty"
            assert len(db_config['password']) >= 8, "Database password too weak (minimum 8 characters)"
            assert db_config['ssl_mode'] in ['require', 'prefer', 'disable'], f"Invalid SSL mode: {db_config['ssl_mode']}"
            assert db_config['max_connections'] > 0, "Max connections must be positive"
            assert db_config['timeout'] > 0, "Database timeout must be positive"
            
        finally:
            os.unlink(config_file)

    def test_security_configuration_violations(self):
        """Test failure with insecure configuration settings"""
        # Set insecure environment variables
        insecure_env = {
            'DEBUG_MODE': 'true',  # Debug enabled in production
            'SECRET_KEY': 'default_secret',  # Default/weak secret
            'DATABASE_PASSWORD': 'password123',  # Weak password
            'API_TOKEN': 'abc123',  # Short API token
            'SSL_DISABLED': 'true',  # SSL disabled
            'CORS_ALLOW_ALL': 'true',  # CORS allows all origins
            'LOG_LEVEL': 'DEBUG',  # Debug logging enabled
            'ENVIRONMENT': 'production'  # This is supposed to be production
        }
        
        for key, value in insecure_env.items():
            os.environ[key] = value
        
        try:
            environment = os.getenv('ENVIRONMENT')
            
            # Security validations that should fail in production
            if environment == 'production':
                debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
                assert not debug_mode, "Debug mode must be disabled in production"
                
                secret_key = os.getenv('SECRET_KEY')
                assert secret_key != 'default_secret', "Default secret key detected in production"
                assert len(secret_key) >= 32, "Secret key too short for production use"
                
                db_password = os.getenv('DATABASE_PASSWORD')
                common_passwords = ['password', 'password123', '123456', 'admin']
                assert db_password not in common_passwords, "Weak database password detected"
                
                api_token = os.getenv('API_TOKEN')
                assert len(api_token) >= 32, "API token too short for secure usage"
                
                ssl_disabled = os.getenv('SSL_DISABLED', 'false').lower() == 'true'
                assert not ssl_disabled, "SSL must not be disabled in production"
                
                cors_allow_all = os.getenv('CORS_ALLOW_ALL', 'false').lower() == 'true'
                assert not cors_allow_all, "CORS cannot allow all origins in production"
                
                log_level = os.getenv('LOG_LEVEL', 'INFO')
                assert log_level != 'DEBUG', "Debug logging must be disabled in production"
            
        finally:
            # Clean up environment variables
            for key in insecure_env.keys():
                os.environ.pop(key, None)

    def test_network_configuration_errors(self):
        """Test failure with invalid network configuration"""
        network_config = {
            'services': {
                'api': {
                    'host': '999.999.999.999',  # Invalid IP address
                    'port': 'not_a_number',  # Non-numeric port
                    'protocol': 'invalid_protocol'  # Invalid protocol
                },
                'database': {
                    'host': 'localhost',
                    'port': 0,  # Invalid port (0)
                    'connection_string': 'postgresql://user@:5432/db'  # Malformed connection string
                },
                'cache': {
                    'host': '',  # Empty host
                    'port': 65536,  # Port out of range
                    'url': 'not_a_valid_url'  # Invalid URL format
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(network_config, f)
            config_file = f.name
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            services = config['services']
            
            # API service validation (should fail)
            api = services['api']
            api_host_parts = api['host'].split('.')
            assert len(api_host_parts) == 4, "Invalid IP address format"
            for part in api_host_parts:
                assert 0 <= int(part) <= 255, f"IP address octet {part} out of range"
            
            assert isinstance(api['port'], int), "API port must be an integer"
            assert api['protocol'] in ['http', 'https', 'tcp', 'udp'], f"Invalid protocol: {api['protocol']}"
            
            # Database service validation (should fail)
            db = services['database']
            assert db['port'] > 0, "Database port must be positive"
            assert '://' in db['connection_string'], "Invalid connection string format"
            assert '@' in db['connection_string'], "Connection string missing credentials separator"
            
            # Cache service validation (should fail)
            cache = services['cache']
            assert len(cache['host'].strip()) > 0, "Cache host cannot be empty"
            assert 1 <= cache['port'] <= 65535, f"Cache port {cache['port']} out of valid range"
            assert cache['url'].startswith(('redis://', 'rediss://')), "Invalid cache URL format"
            
        finally:
            os.unlink(config_file)

    def test_resource_limit_configuration_errors(self):
        """Test failure with invalid resource limit configuration"""
        # Set invalid resource limits
        os.environ['MAX_MEMORY'] = '-1'  # Negative memory
        os.environ['MAX_CPU_CORES'] = '0'  # Zero CPU cores
        os.environ['MAX_CONNECTIONS'] = 'unlimited'  # Invalid format
        os.environ['TIMEOUT_SECONDS'] = '-30'  # Negative timeout
        os.environ['RETRY_ATTEMPTS'] = 'infinity'  # Invalid format
        
        try:
            # Validate memory limits
            max_memory = int(os.getenv('MAX_MEMORY'))
            assert max_memory > 0, "Maximum memory must be positive"
            assert max_memory <= 32 * 1024 * 1024 * 1024, "Maximum memory too large (>32GB)"
            
            # Validate CPU limits
            max_cpu_cores = int(os.getenv('MAX_CPU_CORES'))
            assert max_cpu_cores > 0, "Maximum CPU cores must be positive"
            assert max_cpu_cores <= 128, "Maximum CPU cores too large (>128)"
            
            # Validate connection limits
            max_connections = int(os.getenv('MAX_CONNECTIONS'))
            assert max_connections > 0, "Maximum connections must be positive"
            assert max_connections <= 10000, "Maximum connections too large (>10000)"
            
            # Validate timeout settings
            timeout_seconds = int(os.getenv('TIMEOUT_SECONDS'))
            assert timeout_seconds > 0, "Timeout must be positive"
            assert timeout_seconds <= 3600, "Timeout too large (>1 hour)"
            
            # Validate retry settings
            retry_attempts = int(os.getenv('RETRY_ATTEMPTS'))
            assert retry_attempts >= 0, "Retry attempts cannot be negative"
            assert retry_attempts <= 10, "Too many retry attempts (>10)"
            
        except ValueError as e:
            # This is expected due to invalid values, but we still want the test to fail
            pytest.fail(f"Configuration validation failed due to invalid values: {e}")
        finally:
            # Clean up environment variables
            env_vars = ['MAX_MEMORY', 'MAX_CPU_CORES', 'MAX_CONNECTIONS', 'TIMEOUT_SECONDS', 'RETRY_ATTEMPTS']
            for var in env_vars:
                os.environ.pop(var, None)

    def test_circular_configuration_dependencies(self):
        """Test failure with circular configuration dependencies"""
        config_data = {
            'service_a': {
                'depends_on': ['service_b'],
                'url': '${SERVICE_B_URL}/api'
            },
            'service_b': {
                'depends_on': ['service_c'],
                'url': '${SERVICE_C_URL}/api'
            },
            'service_c': {
                'depends_on': ['service_a'],  # Creates circular dependency
                'url': '${SERVICE_A_URL}/api'
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w