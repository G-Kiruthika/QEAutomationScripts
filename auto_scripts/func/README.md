# Functional UI Automation Framework

## Overview
This is a Python-based Selenium automation framework following Page Object Model (POM) design pattern for functional UI testing.

## Project Structure
```
auto_scripts/func/
├── config/
│   └── config.yaml           # Configuration file
├── core/
│   ├── driver_factory.py     # WebDriver factory
│   ├── error_handler.py      # Error handling and logging
│   └── metadata_validator.py # Metadata validation
├── pages/
│   ├── base_page.py          # Base page class
│   ├── login_page.py         # Login page object
│   └── registration_page.py  # Registration page object
├── tests/
│   └── ui/
│       └── test_login.py     # Login test cases
├── utils/
│   └── git_integration.py    # Git utilities
├── logs/                      # Test execution logs
├── reports/                   # Test reports
├── conftest.py               # Pytest configuration
├── pytest.ini                # Pytest settings
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd auto_scripts/func
   ```

2. Create virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run specific test file:
```bash
pytest tests/ui/test_login.py
```

### Run specific test:
```bash
pytest tests/ui/test_login.py::TestLogin::test_login_blank_username_tc_008
```

### Run with markers:
```bash
pytest -m login
pytest -m smoke
```

### Run in parallel:
```bash
pytest -n auto
```

### Generate HTML report:
```bash
pytest --html=reports/report.html --self-contained-html
```

### Generate Allure report:
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Configuration

Edit `config/config.yaml` to customize:
- Browser settings (chrome, firefox, edge)
- Headless mode
- Timeouts
- Environment URLs
- Test data
- Logging settings

## Framework Features

### Page Object Model (POM)
- Separation of test logic and page elements
- Reusable page classes
- Maintainable and scalable structure

### Driver Factory
- Centralized WebDriver management
- Support for multiple browsers
- Automatic driver installation
- Configurable options

### Error Handling
- Centralized error logging
- Screenshot capture on failure
- Detailed error messages
- Test execution logs

### Metadata Validation
- Validate test metadata structure
- Ensure data integrity
- Support for complex test scenarios

### Git Integration
- Repository status tracking
- Automated commit and push
- Branch management

## Best Practices

1. **Follow POM**: Keep page elements and actions in page classes
2. **Use fixtures**: Leverage pytest fixtures for setup and teardown
3. **Add markers**: Tag tests with appropriate markers
4. **Write assertions**: Use clear and descriptive assertions
5. **Handle waits**: Use explicit waits for dynamic elements
6. **Log appropriately**: Add meaningful log messages
7. **Keep tests independent**: Each test should run independently
8. **Use test data**: Externalize test data in config.yaml

## Troubleshooting

### WebDriver issues:
- Ensure internet connection for automatic driver download
- Check browser version compatibility
- Try clearing webdriver cache

### Test failures:
- Check logs in `logs/` directory
- Review screenshots in `logs/screenshots/`
- Verify element locators
- Check timeouts in config

### Import errors:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version compatibility

## Contributing

1. Create feature branch
2. Make changes following coding standards
3. Add/update tests
4. Run tests locally
5. Submit pull request

## Support

For issues or questions, please contact the QA team or create an issue in the repository.
