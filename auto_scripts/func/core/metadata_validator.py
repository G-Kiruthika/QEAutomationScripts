import json
import os
from typing import Dict, List, Any


class MetadataValidator:
    """Validator for test script metadata"""

    def __init__(self, metadata_path: str = None):
        """Initialize MetadataValidator with metadata file path"""
        self.metadata_path = metadata_path
        self.metadata = None
        if metadata_path and os.path.exists(metadata_path):
            self.load_metadata()

    def load_metadata(self):
        """Load metadata from JSON file"""
        try:
            with open(self.metadata_path, 'r') as file:
                self.metadata = json.load(file)
            return True
        except Exception as e:
            print(f"Error loading metadata: {str(e)}")
            return False

    def validate_metadata_structure(self) -> Dict[str, Any]:
        """Validate the structure of metadata"""
        if not self.metadata:
            return {"valid": False, "errors": ["Metadata not loaded"]}

        errors = []
        
        # Check for required top-level keys
        required_keys = ['test_scripts', 'framework']
        for key in required_keys:
            if key not in self.metadata:
                errors.append(f"Missing required key: {key}")

        # Validate test_scripts structure
        if 'test_scripts' in self.metadata:
            if not isinstance(self.metadata['test_scripts'], list):
                errors.append("test_scripts must be a list")
            else:
                for idx, test_script in enumerate(self.metadata['test_scripts']):
                    test_errors = self._validate_test_script(test_script, idx)
                    errors.extend(test_errors)

        # Validate framework structure
        if 'framework' in self.metadata:
            framework_errors = self._validate_framework(self.metadata['framework'])
            errors.extend(framework_errors)

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def _validate_test_script(self, test_script: Dict, index: int) -> List[str]:
        """Validate individual test script structure"""
        errors = []
        required_fields = ['testCaseId', 'testCaseDescription', 'page', 'steps']
        
        for field in required_fields:
            if field not in test_script:
                errors.append(f"Test script {index}: Missing required field '{field}'")

        # Validate steps
        if 'steps' in test_script:
            if not isinstance(test_script['steps'], list):
                errors.append(f"Test script {index}: 'steps' must be a list")
            else:
                for step_idx, step in enumerate(test_script['steps']):
                    if 'action' not in step:
                        errors.append(f"Test script {index}, step {step_idx}: Missing 'action' field")

        return errors

    def _validate_framework(self, framework: Dict) -> List[str]:
        """Validate framework configuration"""
        errors = []
        
        if 'dependencies' in framework:
            if not isinstance(framework['dependencies'], list):
                errors.append("framework.dependencies must be a list")

        if 'ecosystem_sync' in framework:
            if not isinstance(framework['ecosystem_sync'], dict):
                errors.append("framework.ecosystem_sync must be a dictionary")

        return errors

    def get_test_cases(self) -> List[Dict]:
        """Get all test cases from metadata"""
        if self.metadata and 'test_scripts' in self.metadata:
            return self.metadata['test_scripts']
        return []

    def get_dependencies(self) -> List[str]:
        """Get framework dependencies"""
        if self.metadata and 'framework' in self.metadata:
            return self.metadata['framework'].get('dependencies', [])
        return []

    def get_ecosystem_sync_config(self) -> Dict:
        """Get ecosystem sync configuration"""
        if self.metadata and 'framework' in self.metadata:
            return self.metadata['framework'].get('ecosystem_sync', {})
        return {}
