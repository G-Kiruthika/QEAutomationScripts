"""Database helper utilities for test automation"""
import psycopg2
from typing import Dict, Any, Optional
import yaml

class DatabaseHelper:
    """Helper class for database operations in tests"""
    
    def __init__(self, config_path="config/config.yaml"):
        """Initialize database connection from config"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        db_config = config.get('database', {})
        self.connection = psycopg2.connect(
            host=db_config.get('host', 'localhost'),
            port=db_config.get('port', 5432),
            database=db_config.get('name', 'test_db'),
            user=db_config.get('user', 'test_user'),
            password=db_config.get('password', 'test_password')
        )
        self.cursor = self.connection.cursor()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> list:
        """Execute a database query and return results"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_user_record(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve user record by email"""
        query = "SELECT * FROM users WHERE email = %s"
        result = self.execute_query(query, (email,))
        if result:
            return {
                'email': result[0][0],
                'password_hash': result[0][1],
                'name': result[0][2]
            }
        return None
    
    def verify_password_hash_exists(self, email: str) -> bool:
        """Verify that password hash exists for user"""
        user = self.get_user_record(email)
        return user is not None and user.get('password_hash') is not None
    
    def close(self):
        """Close database connection"""
        self.cursor.close()
        self.connection.close()
