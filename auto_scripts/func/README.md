# Python UI Automation Framework

## Overview
This is a Python-based UI automation framework using Selenium WebDriver and Pytest. The framework follows the Page Object Model (POM) design pattern and includes comprehensive test coverage for login functionality.

## Project Structure
```
auto_scripts/func/
├── config/              # Configuration files
│   └── config.yaml
├── core/                # Core framework utilities
│   ├── driver_factory.py
│   └── selenium_wrapper.py
├── pages/               # Page Object classes
│   ├── login_page.py
│   └── dashboard_page.py
├── tests/               # Test cases
│   ├── conftest.py
│   └── ui/
│       └── test_login.py
├── utils/               # Utility functions
│   ├── test_data_loader.py
│   └── screenshot_helper.py
├── requirements.txt     # Python dependencies
├── pytest.ini          # Pytest configuration
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Chrome or Firefox browser

### Installation
1. Clone the repository
2. Navigate to the project directory:
   ```bash
   cd auto_scripts/func
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Edit `config/config.yaml` to customize:
- Browser settings (Chrome/Firefox, headless mode)
- Base URLs
- Timeouts and waits
- Test data
- Reporting options

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/ui/test_login.py
```

### Run specific test
```bash
pytest tests/ui/test_login.py::test_login_valid_credentials
```

### Run with markers
```bash
pytest -m login
pytest -m smoke
```

### Run in headless mode
Update `config/config.yaml` and set `headless: true`

### Generate HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

## Test Cases

### Login Tests (test_login.py)
1. **test_login_valid_credentials**: Verifies successful login with valid username and password
2. **test_login_invalid_username**: Verifies error message display for invalid username

## Framework Features

### Page Object Model
- Separation of test logic and page interactions
- Reusable page methods
- Maintainable and scalable structure

### Configuration Management
- Centralized configuration in YAML format
- Environment-specific settings
- Easy test data management

### Robust Waits
- Implicit and explicit waits
- Custom wait utilities
- Configurable timeout values

### Screenshot Capture
- Automatic screenshots on test failures
- Manual screenshot capability
- Organized screenshot storage

### Reporting
- HTML test reports
- Detailed test execution logs
- Screenshot attachments on failures

## Best Practices

1. **Follow naming conventions**:
   - Files: lowercase_with_underscores.py
   - Classes: PascalCase
   - Methods: snake_case
   - Tests: test_feature_action

2. **Use Page Object Model**:
   - Keep locators in page classes
   - Implement page methods for interactions
   - Return page objects for method chaining

3. **Write maintainable tests**:
   - One assertion per test (when possible)
   - Clear test names describing functionality
   - Use fixtures for setup and teardown

4. **Handle waits properly**:
   - Use explicit waits over implicit
   - Configure timeouts in config.yaml
   - Implement custom wait conditions when needed

## Troubleshooting

### WebDriver Issues
- Ensure browser drivers are up to date
- Check browser compatibility with Selenium version
- Verify PATH environment variable includes driver location

### Test Failures
- Check screenshots in `screenshots/failures/` directory
- Review test logs for detailed error messages
- Verify test data in config.yaml

### Configuration Issues
- Validate YAML syntax in config.yaml
- Ensure all required fields are present
- Check file paths are correct

## Contributing
1. Follow the existing code structure
2. Adhere to PEP 8 style guidelines
3. Add tests for new functionality
4. Update documentation as needed

## Support
For issues or questions, please contact the QA Automation team.
