# Lab Portal - Deployment Strategy

## Overview
Based on the multi-lab environment and user requirements, this deployment strategy prioritizes ease of deployment and minimal maintenance overhead while providing flexibility for different deployment scenarios.

## Primary Deployment Method: OVA Template

### Why OVA is Perfect for Your Environment:
- **Multi-lab consistency**: Identical deployments across all labs
- **VM-ready infrastructure**: Labs can already spin up VMs
- **Technically minded but not sysadmin users**: Eliminates complex setup
- **Infrequent updates**: OVA suits annual update cycles
- **Self-contained troubleshooting**: All components in one place

### OVA Template Specifications:
```
Base System: Rocky Linux 9.x (minimal)
RAM: 4GB (adjustable)
Storage: 20GB (thin provisioned)
Network: Single interface (DHCP or static)
Default Credentials: admin/ChangeMe123!
```

### Pre-installed Components:
- Rocky Linux 9.x with security updates
- Python 3.11+ with Lab Portal dependencies
- PostgreSQL database with initialized schema
- Nginx reverse proxy (SSL ready)
- Systemd services for automatic startup
- Pre-configured firewall rules
- Lab Portal application with default admin user

### OVA First-Boot Configuration:
1. **Network Setup Wizard**
   - DHCP or static IP configuration
   - Hostname configuration
   - Timezone selection

2. **Security Hardening**
   - Force admin password change on first login
   - Generate new database passwords
   - Create SSL certificates (self-signed or Let's Encrypt ready)

3. **Lab-Specific Setup**
   - Lab name and logo upload
   - Initial device scanning configuration
   - Admin user creation wizard

## Secondary Deployment Method: Podman Container

### When to Use Containers:
- Labs with existing container infrastructure
- Development/testing environments
- Custom deployment requirements
- Integration with existing systems

### Container Configuration:
```yaml
# podman-compose.yml
version: '3'
services:
  lab-portal-web:
    image: lab-portal:latest
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://labportal:password@lab-portal-db:5432/labportal
    volumes:
      - lab-portal-data:/app/data
    depends_on:
      - lab-portal-db

  lab-portal-db:
    image: postgres:15
    environment:
      - POSTGRES_DB=labportal
      - POSTGRES_USER=labportal
      - POSTGRES_PASSWORD=password
    volumes:
      - lab-portal-db-data:/var/lib/postgresql/data

volumes:
  lab-portal-data:
  lab-portal-db-data:
```

## Development Environment: Direct Installation

### For Development and Testing:
- Local Rocky Linux development
- Direct Python environment
- SQLite for rapid prototyping
- Easy debugging and modification

## Distribution Strategy

### Version 1.0 Release Package:
```
lab-portal-v1.0/
├── lab-portal-v1.0.ova                 # Primary distribution
├── lab-portal-container/               # Container option
│   ├── podman-compose.yml
│   ├── lab-portal-latest.tar           # Container image
│   └── README-containers.md
├── documentation/
│   ├── deployment-guide.pdf
│   ├── admin-quickstart.pdf
│   └── troubleshooting-guide.pdf
└── README.md                           # Quick start guide
```

### OVA Distribution Workflow:
1. **Build Base OVA**
   - Automated build pipeline
   - Security hardening
   - Application installation
   - Testing and validation

2. **Version Management**
   - `lab-portal-v1.0.ova` (initial release)
   - `lab-portal-v1.1.ova` (bugfix updates)
   - `lab-portal-v2.0.ova` (major features)

3. **Distribution**
   - Internal company portal download
   - SHA256 checksums for verification
   - Release notes and upgrade guides

## Deployment Workflows

### OVA Deployment (Primary):
```
1. Download lab-portal-v1.0.ova
2. Import into VMware/VirtualBox
3. Power on VM
4. Access https://VM-IP for setup wizard
5. Complete first-boot configuration
6. Start using Lab Portal
```

### Container Deployment (Secondary):
```
1. Install Podman/Docker
2. Download container package
3. Load images: podman load -i lab-portal-latest.tar
4. Run: podman-compose up -d
5. Access http://localhost:8080
```

### Direct Installation (Development):
```
1. Install Rocky Linux 9.x
2. Clone repository
3. Run installation script
4. Configure database
5. Start development server
```

## Update Strategy

### Annual Update Cycle:
- **Major releases**: New OVA with full system refresh
- **Security updates**: Documentation for manual patching
- **Critical fixes**: Emergency patch scripts

### Update Process for OVAs:
1. **Backup current system**
   - Export database
   - Save configuration files
   - Document custom settings

2. **Deploy new OVA**
   - Import new version
   - Run migration scripts
   - Restore data and settings

3. **Validation**
   - Test core functionality
   - Verify device scanning
   - Check admin panel access

## Support and Troubleshooting

### Built-in Diagnostics:
- System health check scripts
- Log aggregation and analysis
- Configuration validation tools
- Network connectivity tests

### Support Documentation:
- **Quick Start Guide**: 2-page getting started
- **Admin Guide**: Complete administration manual
- **Troubleshooting Guide**: Common issues and solutions
- **API Reference**: For advanced integrations

### Remote Support Ready:
- SSH access for troubleshooting
- Log export functionality
- Configuration backup/restore
- Remote diagnostic scripts

## Technical Implementation Plan

### Phase 1: Core Development (Direct Installation)
- Develop using TDD approach
- Local Rocky Linux environment
- SQLite for rapid iteration
- Complete all 10 functions

### Phase 2: Containerization
- Create Dockerfiles/Containerfiles
- Multi-container setup with database
- Volume management for persistence
- Container networking configuration

### Phase 3: OVA Creation
- Automated OVA build pipeline
- Base system hardening
- Application installation scripts
- First-boot configuration wizard
- Testing and validation automation

### Phase 4: Distribution
- Create download portal
- Generate documentation
- Release management process
- User feedback collection system

## Success Metrics

### Deployment Success:
- **Time to Deploy**: < 30 minutes from download to working system
- **User Satisfaction**: Deployment difficulty rating
- **Support Requests**: Track common deployment issues

### Operational Success:
- **System Uptime**: Monitor lab portal availability
- **Update Success Rate**: Track successful updates
- **User Adoption**: Number of active lab deployments

## Risk Mitigation

### Deployment Risks:
- **VM Resource Constraints**: Provide sizing guidelines
- **Network Configuration**: Pre-configure common setups
- **Security Concerns**: Built-in hardening and documentation

### Update Risks:
- **Data Loss**: Automated backup procedures
- **Downtime**: Minimal downtime update process
- **Compatibility**: Thorough testing before release

### Support Risks:
- **Knowledge Transfer**: Comprehensive documentation
- **Troubleshooting**: Remote diagnostic capabilities
- **Scalability**: Clear capacity planning guidelines

---

*This strategy ensures maximum adoption across multiple labs while minimizing support overhead and deployment complexity.*
