# Lab Portal - Test-Driven Development Strategy

## Overview
This document outlines the Test-Driven Development (TDD) approach for the Lab Portal Management System. TDD will help ensure code quality, reduce bugs, and provide confidence when making changes throughout development.

## TDD Principles for This Project

### Red-Green-Refactor Cycle
1. **Red**: Write a failing test for the next small piece of functionality
2. **Green**: Write the minimal code needed to make the test pass
3. **Refactor**: Improve the code while keeping tests green

### Test-First Mindset
- Always write tests before implementation code
- Think about the expected behavior before writing the solution
- Use tests as living documentation of system requirements

## Testing Framework Stack

### Backend Testing (Python)
- **Primary Framework**: pytest
- **Database Testing**: pytest-django or SQLAlchemy testing utilities
- **API Testing**: requests or httpx for endpoint testing
- **Mock/Stub**: unittest.mock or pytest-mock
- **Coverage**: pytest-cov for coverage reporting

### Frontend Testing (JavaScript)
- **Unit Testing**: Jest or Vitest
- **DOM Testing**: Testing Library
- **End-to-End**: Playwright or Cypress
- **Component Testing**: Testing Library with React/Vue testing utilities

### Integration Testing
- **Database**: Test database with fixtures
- **External APIs**: Mock external services (VMware, DHCP)
- **Authentication**: Test PAM integration with test users

## Test Organization Structure

```
/tests/
├── unit/                   # Fast, isolated tests
│   ├── auth/              # Authentication module tests
│   ├── devices/           # Device management tests
│   ├── scanning/          # Network scanner tests
│   └── utils/             # Utility function tests
├── integration/           # Tests that combine multiple components
│   ├── auth_flow/         # Complete authentication workflows
│   ├── device_management/ # End-to-end device operations
│   └── admin_panel/       # Admin functionality integration
├── e2e/                   # End-to-end browser tests
│   ├── user_journeys/     # Complete user workflows
│   └── admin_workflows/   # Admin task completion
├── fixtures/              # Test data and setup
│   ├── users.py          # Test user data
│   ├── devices.py        # Sample device data
│   └── network_responses.py # Mock network responses
└── conftest.py           # Pytest configuration and fixtures
```

## Function-by-Function Testing Strategy

### Function #1: Multi-Level Authentication System

**Test Categories:**
```python
# Unit Tests
def test_pam_authentication_success()
def test_pam_authentication_failure()
def test_database_user_creation()
def test_password_validation()
def test_session_management()

# Integration Tests  
def test_login_flow_pam_user()
def test_login_flow_database_user()
def test_logout_flow()
def test_session_persistence()

# Security Tests
def test_unauthorized_access_blocked()
def test_session_timeout()
def test_password_hashing()
```

### Function #2: Admin Panel/Dashboard

**Test Categories:**
```python
# Unit Tests
def test_admin_user_detection()
def test_admin_menu_rendering()
def test_admin_permission_checks()

# Integration Tests
def test_admin_dashboard_access()
def test_non_admin_blocked_from_admin()
def test_admin_crud_operations()

# UI Tests
def test_admin_navigation_visible()
def test_admin_forms_validation()
```

### Function #3: DHCP Service Management

**Test Categories:**
```python
# Unit Tests
def test_dhcp_lease_parsing()
def test_reservation_validation()
def test_ip_range_validation()

# Integration Tests
def test_dhcp_api_connection()
def test_lease_retrieval()
def test_reservation_creation()

# Mock Tests (for external API)
def test_dhcp_service_unavailable()
def test_dhcp_api_timeout()
```

### Function #4: Network Device Scanner

**Test Categories:**
```python
# Unit Tests
def test_ip_range_parsing()
def test_device_discovery_logic()
def test_mac_oui_lookup()
def test_vmware_detection()

# Integration Tests
def test_full_network_scan()
def test_dhcp_integration()
def test_vmware_api_integration()

# Performance Tests
def test_scan_timeout_handling()
def test_concurrent_scanning()
```

### Function #5: Device Management System

**Test Categories:**
```python
# Unit Tests
def test_device_group_creation()
def test_device_assignment()
def test_ownership_inheritance()

# Integration Tests
def test_device_lifecycle()
def test_group_deletion_handling()
def test_testdrive_group_behavior()

# Business Logic Tests
def test_vm_host_group_creation()
def test_ownership_notification_system()
```

## Test Data Management

### Fixtures and Test Data
```python
# conftest.py
@pytest.fixture
def test_users():
    return {
        'admin': {'username': 'admin_test', 'is_admin': True},
        'user': {'username': 'user_test', 'is_admin': False},
        'pam_user': {'username': 'pam_test', 'auth_type': 'pam'}
    }

@pytest.fixture
def sample_devices():
    return [
        {'ip': '192.168.1.100', 'mac': '00:11:22:33:44:55', 'type': 'UPS'},
        {'ip': '192.168.1.101', 'mac': '00:11:22:33:44:56', 'type': 'PDU'}
    ]

@pytest.fixture
def mock_vmware_api():
    # Mock VMware API responses
    pass
```

### Database Testing
```python
# Use test database for all tests
@pytest.fixture(scope="session")
def test_db():
    # Create test database
    # Run migrations
    # Yield database connection
    # Clean up after tests
```

## Coverage Targets

### Minimum Coverage Requirements
- **Unit Tests**: 90% code coverage
- **Critical Paths**: 100% coverage for authentication, security, data integrity
- **Integration Tests**: Cover all user workflows
- **E2E Tests**: Cover complete user journeys

### Coverage Monitoring
```bash
# Run tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Coverage targets by module
# auth: 95%
# devices: 90%
# scanning: 85%
# admin: 90%
```

## Development Workflow

### Daily TDD Workflow
1. **Morning**: Review failing tests from previous day
2. **Feature Work**: 
   - Write test for next small feature
   - Run test (should fail)
   - Write minimal code to pass
   - Refactor if needed
   - Commit when green
3. **End of Day**: Run full test suite, commit clean state

### Test Categories by Development Phase

**Phase 1: Foundation (Weeks 1-2)**
- Authentication unit tests
- Basic database operations
- Core utility functions

**Phase 2: Core Features (Weeks 3-4)**
- Device scanning integration tests
- Admin panel functionality
- DHCP integration

**Phase 3: User Experience (Weeks 5-6)**
- Frontend component tests
- User journey tests
- Performance tests

**Phase 4: Polish (Week 7)**
- Edge case testing
- Error handling tests
- Security testing

## Testing Tools Configuration

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --disable-warnings
    --cov=app
    --cov-report=term-missing
    --cov-report=html:htmlcov
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow tests that can be skipped in development
```

### Test Environment Setup
```python
# tests/conftest.py
import pytest
from app import create_app
from app.database import db

@pytest.fixture(scope="session")
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
```

## Debugging and Troubleshooting

### Common Test Failure Patterns
1. **Red Tests That Should Be Green**: Check test logic, not implementation
2. **Intermittent Failures**: Usually timing or state issues
3. **Slow Tests**: Mock external dependencies, optimize database operations

### Debugging Tools
```python
# Add debugging to tests
import pdb; pdb.set_trace()  # Python debugger
pytest --pdb  # Drop into debugger on failure
pytest -s  # Show print statements
pytest -vv  # Very verbose output
```

### Test Isolation
- Each test should be independent
- Clean database state between tests
- Mock external services
- Use fixtures for consistent test data

## Success Metrics

### Code Quality Indicators
- **Test Coverage**: >90% overall, >95% for critical components
- **Test Speed**: Unit tests <1s, integration tests <10s
- **Test Reliability**: <1% flaky test rate
- **Bug Detection**: Tests catch >95% of bugs before deployment

### Development Confidence Indicators
- **Refactoring Safety**: Can change code structure without fear
- **Feature Addition**: New features don't break existing functionality
- **Debugging Speed**: Issues can be isolated quickly through failing tests
- **Code Understanding**: New team members can understand code through tests

## Learning Resources for TDD

### Recommended Reading
- "Test Driven Development: By Example" by Kent Beck
- "Growing Object-Oriented Software, Guided by Tests" by Freeman & Pryce
- "Architecture Patterns with Python" by Percival & Gregory

### Practice Exercises
- Start with simple utility functions
- Practice the Red-Green-Refactor cycle
- Write tests for existing code to understand testing patterns

## Documentation Integration

### Test Documentation
- Each test file includes purpose and scope comments
- Complex test scenarios include step-by-step comments
- Integration tests document the workflow being tested

### Living Documentation
- Tests serve as examples of how code should be used
- Test names clearly describe the expected behavior
- Test data represents realistic use cases

---

*This strategy will evolve as the project progresses. Regular retrospectives will help refine the approach based on what works best for the Lab Portal development.*
