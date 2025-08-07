# Lab Portal Management System

A comprehensive web-based laboratory management system designed for network device monitoring, management, and public equipment access. Built with Test-Driven Development (TDD) principles and designed for multi-lab deployment.

## Overview

The Lab Portal Management System provides a centralized platform for managing laboratory networks, devices, and user access. It combines network discovery, device management, user authentication, and public equipment showcasing in a single, easy-to-deploy application.

## Key Features

### 🔐 Multi-Level Authentication
- PAM (Linux system) authentication integration
- Database-stored user accounts
- Role-based access control (Admin, Registered, Unregistered)

### 📊 Admin Dashboard
- Comprehensive management interface
- Real-time system monitoring
- Configuration management tools

### 🌐 DHCP Service Management
- KEA DHCP server integration
- Lease management and monitoring
- Reservation configuration

### 🔍 Network Device Scanner
- Automated network discovery
- VMware integration (vCenter/ESXi)
- Protocol detection (SNMP, Modbus TCP)
- Scheduled scanning with configurable intervals

### 📱 Device Management System
- Intelligent device grouping and organization
- Ownership tracking and notifications
- Public "Testdrive" device showcase
- VMware host/guest relationship mapping

### 💬 Dynamic Help and Feedback System
- Context-aware help content
- User feedback collection and management
- Built-in documentation system

### 🏠 Public Landing Page
- Professional, responsive design
- Real-time device status display
- Admin-configurable content and branding

### 👥 User Management
- **Unregistered Users**: Public device viewing, registration, help access
- **Registered Users**: Enhanced features, feedback submission, tools access
- **Admin Users**: Full system management and configuration

### 🛠️ Device Interaction Tools
- Network probing and diagnostics
- Configuration backup and management
- Admin-managed tool library

## Documentation

This project includes comprehensive documentation covering all aspects of development, testing, and deployment:

### 📋 [Functional Requirements](FUNCTIONAL_REQUIREMENTS.md)
Complete specification of all 10 system functions including:
- User stories and acceptance criteria
- Technical implementation details
- Dependencies and integration points
- Questions and decision points for implementation

### 🧪 [Test Strategy](TEST_STRATEGY.md)
Comprehensive Test-Driven Development approach covering:
- Testing frameworks and tools
- Test organization structure
- Function-by-function testing strategy
- Coverage targets and quality metrics
- Development workflow and best practices

### 🚀 [Deployment Strategy](DEPLOYMENT_STRATEGY.md)
Multi-option deployment approach including:
- **OVA Template**: Plug-and-play virtual appliance (recommended for production)
- **Podman Container**: Containerized deployment for flexibility
- **Direct Installation**: Development and learning environment
- Distribution strategy and update procedures

## Target Environment

- **Operating System**: Rocky Linux 9.x
- **Deployment**: Multi-lab environment with VM infrastructure
- **Users**: Technically minded lab administrators
- **Update Frequency**: Annual major releases with occasional patches

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI or Flask
- **Database**: PostgreSQL (production), SQLite (development)
- **Authentication**: PAM integration + database users
- **Task Scheduling**: Celery or APScheduler

### Frontend
- **Framework**: Modern CSS framework (Bootstrap/Tailwind)
- **Design**: Desktop-focused, responsive
- **Accessibility**: WCAG 2.1 AA compliance
- **Browser Support**: Modern browsers with progressive enhancement

### Infrastructure
- **Containerization**: Podman/Docker support
- **Web Server**: Nginx reverse proxy
- **Network**: DHCP (KEA), VMware API integration
- **Monitoring**: Built-in health checks and diagnostics

## Development Approach

This project follows **Test-Driven Development (TDD)** principles:

1. **Red**: Write failing tests for new functionality
2. **Green**: Implement minimal code to pass tests
3. **Refactor**: Improve code while maintaining test coverage

### Development Phases
1. **Phase 1**: Core development with direct installation
2. **Phase 2**: Containerization and testing
3. **Phase 3**: OVA creation and automation
4. **Phase 4**: Documentation and distribution

## Getting Started

### For Development
1. Set up Rocky Linux 9.x development environment
2. Follow the direct installation guide in [Deployment Strategy](DEPLOYMENT_STRATEGY.md)
3. Review [Test Strategy](TEST_STRATEGY.md) for TDD workflow
4. Implement functions according to [Functional Requirements](FUNCTIONAL_REQUIREMENTS.md)

### For Production Deployment
1. Download the Lab Portal OVA template
2. Import into your virtualization platform
3. Follow the first-boot configuration wizard
4. Access the web interface and complete setup

### For Development/Testing
1. Use Podman container deployment
2. Follow container setup in [Deployment Strategy](DEPLOYMENT_STRATEGY.md)
3. Access development environment

## Project Structure

```
lab_portal/
├── README.md                      # This file
├── FUNCTIONAL_REQUIREMENTS.md     # Complete system specification
├── TEST_STRATEGY.md              # TDD approach and testing guidelines
├── DEPLOYMENT_STRATEGY.md        # Multi-option deployment guide
├── app/                          # Application source code (to be created)
├── tests/                        # Test suite (to be created)
├── docs/                         # Additional documentation (to be created)
├── deployment/                   # Deployment scripts and configs (to be created)
│   ├── ova/                     # OVA build automation
│   ├── containers/              # Container configurations
│   └── scripts/                 # Installation and setup scripts
└── examples/                     # Configuration examples (to be created)
```

## Contributing

This project is designed for internal company use across multiple laboratories. Development follows these principles:

- **Test-Driven Development**: All features must include comprehensive tests
- **Documentation First**: Features are documented before implementation
- **Multi-Lab Compatibility**: Solutions must work across different lab environments
- **Ease of Deployment**: Deployment complexity is minimized for non-sysadmin users

## Support and Documentation

### Built-in Help System
The application includes a comprehensive help system with:
- Context-aware documentation
- Role-based content filtering
- Troubleshooting guides
- API reference for advanced integrations

### Administrative Documentation
- **Quick Start Guide**: Get running in under 30 minutes
- **Admin Manual**: Complete system administration guide
- **Troubleshooting Guide**: Common issues and solutions
- **API Documentation**: For custom integrations

## Version Strategy

- **Major Releases**: Annual updates with new features (v1.0, v2.0)
- **Minor Releases**: Quarterly updates with improvements (v1.1, v1.2)
- **Patch Releases**: Critical fixes as needed (v1.1.1, v1.1.2)

Each release includes:
- Updated OVA template with full system refresh
- Container images for all supported platforms
- Comprehensive migration guides and tools
- Updated documentation and help content

## License

This project is developed for internal company use. All rights reserved.

## Security Considerations

- **Authentication**: Multi-level authentication with PAM integration
- **Authorization**: Role-based access control throughout
- **Network Security**: Configurable firewall rules and SSL/TLS support
- **Data Protection**: Secure credential storage and session management
- **Audit Logging**: Comprehensive activity tracking for security analysis

## Contact and Support

For technical support, feature requests, or deployment assistance, please use the built-in feedback system or contact the development team through your organization's standard channels.

---

**Status**: Planning and Design Phase  
**Next Milestone**: Begin TDD development with Function #1 (Authentication System)  
**Target**: Version 1.0 OVA release for multi-lab deployment
