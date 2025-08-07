# Lab Portal - Functional Requirements Document

## Project Overview
**Project Name:** Lab Portal Management System  
**Document Version:** 1.0  
**Date:** August 6, 2025  
**Status:** Draft - Requirements Gathering Phase

**Target Platform:** Web Application  
**Deployment Environment:** Linux Server (Rocky Linux 9.6)  
**Application Type:** Multi-user web-based laboratory management system

## Purpose
This document outlines the functional requirements for the Lab Portal Management System, detailing each feature and capability that the system should provide.

---

## Functional Requirements

### 1. Multi-Level Authentication System
**Priority:** High  
**Category:** User Management

**Description:**
A hybrid authentication system supporting three distinct user levels with different authentication methods:
- **Unregistered Users:** Public access to landing page only
- **Registered Users:** Database-authenticated users with access to tools and device monitoring
- **Admin Users:** PAM-authenticated users (existing sudo users) with full administrative access

**User Stories:**
- As an unregistered visitor, I want to view the lab portal landing page so that I can see general information about the lab
- As an unregistered visitor, I want to see devices in the "Testdrive" group on the landing page so that I can see what equipment is publicly available
- As an unregistered visitor, I want to see landing page devices sorted by device type so that I can easily find the type of equipment I need
- As a registered user, I want to log in with my portal credentials so that I can access monitoring tools and device status
- As an admin user, I want to log in using my server credentials so that I can access all features and administrative functions
- As an admin, I want to manage registered users so that I can control access to lab resources

**Acceptance Criteria:**
- [ ] Landing page accessible without authentication
- [ ] Display "Testdrive" group devices on landing page for all users (including unregistered)
- [ ] Landing page devices sorted by device type for easy browsing
- [ ] Device information displayed: name, type, description, status (basic info only)
- [ ] User registration system for creating database-stored accounts
- [ ] Database authentication for registered users (username/password)
- [ ] PAM integration for admin users using existing server accounts
- [ ] Role-based access control distinguishing between user levels
- [ ] Session management with appropriate timeouts
- [ ] Secure password handling and storage
- [ ] Admin panel accessible only to PAM-authenticated users

**Technical Notes:**
- **PAM Integration:** Use Python PAM library or subprocess calls to authenticate against system accounts
- **Database Auth:** Secure password hashing (bcrypt/argon2) for registered users
- **Session Management:** JWT tokens or server-side sessions
- **Security:** HTTPS required, password complexity requirements
- **Dual Auth Flow:** System must detect authentication method based on user type
- **Landing Page Integration:** Query "Testdrive" device group for public device display
- **Device Display:** Show basic device information (name, type, description, status) on landing page
- **Sorting:** Sort landing page devices by device type for organized display

**Dependencies:**
None - this is foundational functionality
**Note:** Landing page device display requires Function #5 (Device Management System) for "Testdrive" group device data

**Notes/Questions:**
- Should admin users also be able to create database accounts, or only authenticate via PAM?
- What should happen if a username exists in both PAM and database?
- Should there be a way to "promote" a registered user to admin status?
- **Landing Page Display:** What device information should be shown on the landing page (name, type, description, status)?
- **Device Privacy:** Should any device details be hidden from unregistered users on the landing page?

---

### 2. Admin Panel/Dashboard
**Priority:** High  
**Category:** Administration

**Description:**
A dedicated administrative interface accessible only to PAM-authenticated admin users. This panel serves as the central hub for all administrative functions including user management, system configuration, device management, and administrative tools. The admin panel should have a distinct interface from the regular user portal.

**User Stories:**
- As an admin user, I want to access a dedicated admin panel so that I can manage all administrative functions in one place
- As an admin user, I want the admin panel to be clearly separated from regular user functions so that administrative tasks are organized and secure
- As an admin user, I want to see an overview dashboard of system status, user activity, and device health when I enter the admin panel
- As an admin user, I want to see service status information on the dashboard so that I can quickly identify system issues
- As an admin user, I want to see DHCP service status and VMware host authentication status for devices I own so that I can monitor my assigned infrastructure
- As an admin user, I want service status updated hourly with last update timestamps so that I have current information for troubleshooting
- As an admin user, I want to see recent ownership changes for devices assigned to me so that I can track my responsibility changes
- As an admin user, I want to acknowledge ownership changes so that they are removed from my dashboard once I'm aware of them
- As an admin user, I want to see inactive devices (inactive for 48+ hours) sorted by my ownership vs others so that I can identify potential issues with my assigned devices
- As an admin user, I want to remove devices that are no longer on the network so that I can clean up obsolete device entries
- As an admin user, I want to see new devices detected by the network scanner since my last login so that I can organize them appropriately
- As an admin user, I want to see only unassigned new devices (devices still in "Unassigned Devices" group) so that I focus on devices that need attention
- As an admin user, I want the dashboard to auto-refresh hourly with manual refresh capability so that I have current information without waiting
- As an admin user, I want simple service status indicators with detailed information available on-demand so that I can quickly assess system health
- As an admin user, I want to manage device types in the admin panel so that I can customize device categorization options
- As a regular user, I want to be prevented from accessing admin functions so that system security is maintained

**Acceptance Criteria:**
- [ ] Admin panel accessible only to PAM-authenticated users
- [ ] Clear navigation structure for administrative functions
- [ ] Admin dashboard with comprehensive system overview and personalized information
- [ ] Service status monitoring with hourly updates and last update timestamps:
  - [ ] DHCP service status (active/inactive/error with details)
  - [ ] VMware host authentication status for user's owned devices
  - [ ] Network scanner service status and last scan information
  - [ ] Database connectivity and performance status
  - [ ] Web application service health and resource usage
- [ ] Recent ownership changes display (devices added to or removed from current admin user's ownership)
- [ ] Ownership change acknowledgment system (user can acknowledge changes to remove from dashboard)
- [ ] Unacknowledged ownership changes remain visible until manually acknowledged
- [ ] Inactive device alerts (devices inactive for 48+ hours from network scanner, fixed threshold):
  - [ ] Devices owned by current admin user (priority section)
  - [ ] Devices owned by other users (secondary section)
  - [ ] Device details: name, type, last seen timestamp, owner information
- [ ] Device removal capability for obsolete/decommissioned devices (admin can permanently remove devices no longer on network)
- [ ] New device detection alerts (devices detected by network scanner since user's last login):
  - [ ] Display devices added to "Unassigned Devices" group since last login
  - [ ] Only show devices that remain in "Unassigned Devices" (filter out devices that have been reassigned)
  - [ ] Device details: name, IP, MAC address, device type, detection timestamp
  - [ ] Clear indication of detection date/time for each new device
- [ ] Dashboard auto-refresh (hourly) with manual refresh button for immediate updates
- [ ] Simple service status indicators with click-through for detailed information:
  - [ ] Green/Yellow/Red status indicators for quick assessment
  - [ ] Detailed metrics, error logs, and troubleshooting information accessible via click/expand
  - [ ] Service-specific details: uptime, last check time, error messages, performance metrics
- [ ] Device type management interface (create, edit, delete device types)
- [ ] Separate URL structure (/admin/* or similar) for admin functions
- [ ] Admin-specific UI design/theme to distinguish from user portal
- [ ] Breadcrumb navigation for admin sections
- [ ] Admin activity logging for security auditing
- [ ] Graceful access denial for non-admin users with appropriate error messages

**Technical Notes:**
- **URL Structure:** /admin/* routes protected by admin authentication middleware
- **UI Framework:** Consistent but distinct design from main portal
- **Security:** All admin routes require PAM authentication verification
- **Logging:** Admin actions should be logged for audit trail
- **Navigation:** Modular design to easily add new admin functions
- **Dashboard Features:**
  - **Service Status Monitoring:** Hourly automated checks with timestamp tracking
    - DHCP service status via systemctl and service health checks
    - VMware host authentication status for user-owned devices (from Function #4 data)
    - Network scanner service status and last successful scan timestamps
    - Database connectivity testing and query performance metrics
    - Web application health checks (memory usage, CPU, disk space)
  - **Ownership Change Tracking:** Database queries for recent device ownership modifications
  - **Ownership Change Acknowledgment:** User acknowledgment system to remove changes from dashboard display
  - **Inactive Device Detection:** Cross-reference network scanner data with ownership information (fixed 48-hour threshold)
  - **Device Lifecycle Management:** Permanent device removal capability for decommissioned/obsolete devices
  - **New Device Detection:** Track devices added since user's last login
    - Query devices added to "Unassigned Devices" group after last login timestamp
    - Filter out devices that have been moved from "Unassigned Devices" to other groups
    - Display device details: name, IP, MAC, type, first detection timestamp
    - User login timestamp tracking for comparison with device detection times
  - **Personalized Display:** Filter dashboard information based on current admin user's device ownership
- **Performance:** Dashboard data cached with hourly refresh cycle to minimize system load
- **User Experience:** Auto-refresh dashboard hourly with manual refresh button for immediate updates
- **Status Display:** Simple status indicators (Green/Yellow/Red) with expandable detailed information
- **Responsive Design:** Dashboard optimized for various screen sizes and quick information access

**Dependencies:**
- Function #1: Multi-Level Authentication System

**Notes/Questions:**
- Should the admin panel be a completely separate application or integrated into the main portal?
- What specific admin functions do you want to include? (This will help structure the admin panel sections)
- Do you want real-time updates on the admin dashboard or is periodic refresh sufficient?
- **Service Status Monitoring:** What additional services should be monitored beyond DHCP and VMware hosts?
  - Network scanner background service status
  - Database connectivity and performance
  - Web application health (memory, CPU, disk usage)
  - External service dependencies (if any)
- **Dashboard Refresh:** ✅ Auto-refresh hourly with manual refresh button for immediate updates
- **Inactive Device Threshold:** ✅ Fixed 48-hour threshold with device removal capability for obsolete devices
- **Ownership Change History:** ✅ User acknowledgment system removes changes from dashboard (no time limit, acknowledgment-based)
- **Service Status Details:** ✅ Simple status indicators (Green/Yellow/Red) with click-through for detailed metrics/error information

---

### 3. DHCP Service Management
**Priority:** High  
**Category:** Administration

**Description:**
Administrative interface for managing DHCP service on the server. Admins need to add, remove, and modify DHCP reservations as lab devices are frequently added and removed from the network. The system should provide a web-based interface for managing DHCP configuration without requiring direct server access.

**User Stories:**
- As an admin user, I want to view all current DHCP leases so that I can see what devices are on the network
- As an admin user, I want to create static DHCP reservations for lab devices so that they always get the same IP address
- As an admin user, I want to modify or remove DHCP reservations so that I can manage devices being added/removed from the lab
- As an admin user, I want to configure DHCP pools and options so that I can manage network segments
- As an admin user, I want to restart/reload the DHCP service so that configuration changes take effect
- As an admin user, I want to view DHCP logs and statistics so that I can troubleshoot network issues

**Acceptance Criteria:**
- [ ] Display current DHCP leases (active, expired, reserved)
- [ ] Create new static DHCP reservations (MAC → IP mapping)
- [ ] Edit existing DHCP reservations
- [ ] Delete DHCP reservations
- [ ] Configure DHCP pools (IP ranges, subnet options)
- [ ] Manage DHCP server configuration (lease time, DNS servers, etc.)
- [ ] Start/stop/restart DHCP service
- [ ] View DHCP service status and statistics
- [ ] Display DHCP logs with filtering capabilities
- [ ] Validate MAC addresses and IP ranges
- [ ] Backup/restore DHCP configuration

**Technical Notes:**
- **DHCP Server Integration:** Interface with KEA DHCP via REST API or config file management
- **Configuration Management:** Parse and modify DHCP configuration files
- **Service Control:** Use systemctl commands to manage DHCP service (requires system privileges)
- **Validation:** IP address and MAC address validation
- **Logging:** Parse DHCP logs for display in web interface
- **Security:** All DHCP management operations require PAM authentication (admin-level access)
- **Privilege Escalation:** Web application may need sudo privileges for DHCP service management
- **PAM Integration:** Critical dependency - admin users must be authenticated via PAM before accessing DHCP functions

**Dependencies:**
- Function #1: Multi-Level Authentication System (specifically PAM integration)
- Function #2: Admin Panel/Dashboard
- **Critical:** PAM authentication must be fully functional before DHCP management can be implemented

**Notes/Questions:**
- Should the system support multiple DHCP scopes/subnets?
- Do you need DHCP failover/high availability features?
- Should there be approval workflows for DHCP changes or direct modification?
- What level of DHCP logging detail do you need in the web interface?

### 4. Network Device Scanner
**Priority:** High  
**Category:** Administration

**Description:**
An intelligent network scanner that discovers devices on the lab network with configurable scanning parameters. The scanner integrates with DHCP services to determine IP assignment methods and can identify VMware guest systems. Supports both manual and automated recurring scans with customizable intervals. This function focuses purely on network discovery and data collection.

**User Stories:**
- As an admin user, I want to scan specific IP ranges to discover active devices on the network
- As an admin user, I want to configure recurring scans with custom intervals so that device discovery is automated
- As an admin user, I want to see which devices use static vs DHCP-assigned IPs so that I can manage IP allocation efficiently
- As an admin user, I want to identify VMware guest systems so that I can distinguish between physical and virtual devices
- As an admin user, I want to see device details (hostname, MAC address, vendor) so that I can properly identify and categorize devices
- As an admin user, I want to configure VMware authentication for VM hosts so that the scanner can access detailed VM information
- As an admin user, I want to see the authentication status of VM hosts so that I know which ones are fully accessible
- As an admin user, I want to view scan history and detect changes so that I can track network evolution over time

**Acceptance Criteria:**
- [ ] Configure IP ranges for scanning (single IPs, CIDR blocks, custom ranges)
- [ ] Manual on-demand network scanning
- [ ] Automated recurring scans with configurable intervals (default: 1 hour, minimum: 15 minutes, maximum: 24 hours)
- [ ] Device discovery showing: IP, MAC address, hostname, vendor (OUI lookup)
- [ ] Host detection using ICMP ping scanning (primary method)
- [ ] Optional ARP scanning for additional MAC address discovery
- [ ] Optional MAC OUI vendor lookup for device identification
- [ ] SNMP protocol detection on port 161 (UDP) - confirm protocol response and version (v1/v2c/v3)
- [ ] Modbus TCP protocol detection on port 502 (TCP) - confirm protocol response
- [ ] Protocol detection uses standard ports only (SNMP: 161/UDP, Modbus TCP: 502/TCP)
- [ ] Protocol detection rescanning interval: 6 hours (independent of main device scanning)
- [ ] Protocol detection timeout: 10 seconds (same as main device scanning)
- [ ] DHCP integration to identify static vs dynamic IP assignments
- [ ] DHCP reservation status (reserved vs dynamic lease)
- [ ] VMware guest detection (identify VMs running on detected ESXi hosts)
- [ ] VMware host mapping (show which ESXi host each VM is running on)
- [ ] Device categorization (physical, virtual, network equipment)
- [ ] VMware host detection without authentication (network fingerprinting)
- [ ] VMware host status indicators (detected/authentication required/authenticated/failed)
- [ ] Admin notification workflow for newly detected VMware hosts requiring configuration
- [ ] VMware host authentication configuration interface (per-host credentials and owner assignment)
- [ ] VMware authentication status tracking (detected/configured/authenticated/failed)
- [ ] Authentication testing and validation for VM hosts
- [ ] Option to skip VMware API integration for detected hosts (treat as basic network device)
- [ ] Device type management (create, edit, delete custom device types)
- [ ] Scan history and change detection (new devices, disappeared devices)
- [ ] Performance monitoring (scan duration, device response times)
- [ ] Fixed scan parameters (10-second timeout, 10 concurrent threads)

**Technical Notes:**
- **Network Scanning:** Primary ICMP ping scanning for host detection, with optional ARP scanning and MAC OUI lookup
- **Protocol Detection:** 
  - SNMP protocol detection on port 161 (UDP) - confirm active response and identify version (v1/v2c/v3)
  - Modbus TCP protocol detection on port 502 (TCP) - confirm active response
  - Standard ports only (no non-standard port scanning)
  - Protocol detection for availability confirmation only (no data retrieval or authentication)
  - Protocol detection rescanning interval: 6 hours (independent of main device scanning)
  - Protocol detection timeout: 10 seconds (consistent with main scanning)
  - Protocol detection results stored for informational purposes (not used for device categorization)
- **DHCP Integration:** Query KEA DHCP API for lease information and reservations
- **VMware Detection:** 
  - Network fingerprinting for VMware host detection (no authentication required)
  - VMware host status tracking: Detected → Authentication Required → Configured → Authenticated/Failed
  - Admin notification workflow for newly detected VMware hosts
  - Configuration interface for VMware host credentials and device ownership assignment
  - Optional VMware API integration (admin can choose to skip VM discovery)
  - vCenter Server API integration for managed ESXi host and VMs (when authenticated)
  - Direct ESXi host API integration for standalone ESXi host (when authenticated)
  - MAC address OUI identification for VMware virtual NICs (00:50:56, 00:0C:29, 00:1C:14)
    - Backup VM detection when ICMP ping fails (firewalled VMs)
    - VM vs physical device categorization
    - Cross-reference validation for detected devices
- **VMware Environment:** Support for hybrid setup:
  - One vCenter Server managing one ESXi host
  - One standalone ESXi host (direct API access)
- **VMware Authentication Requirements:**
  - VMware host detection without authentication (network fingerprinting phase)
  - Admin workflow for VMware host configuration:
    - Device owner assignment (required for all VMware hosts)
    - VMware credentials configuration (optional - for VM discovery)
    - Authentication testing and validation
    - Option to skip API integration (treat as basic network device)
  - Multi-phase VMware host status tracking:
    - "Detected" - VMware host found via network fingerprinting
    - "Authentication Required" - Awaiting admin configuration
    - "Configured" - Credentials and owner assigned
    - "Authenticated" - VMware API access successful
    - "Authentication Failed" - VMware API access failed
    - "Basic Device" - Admin chose to skip VMware integration
  - vCenter Server: Username/password or service account credentials
  - Standalone ESXi: Direct host username/password (root or dedicated account)
  - Per-host credential configuration and management
  - Secure credential storage in application database (encrypted)
  - Optional: Read-only service accounts for security
- **VMware Data Retrieved:**
  - VM inventory with host mapping
  - VM network configuration and IP addresses
  - ESXi host information and resource usage
- **Scheduling:** Background task system (Celery, APScheduler, or cron integration)
- **Performance:** Fixed threading (10 concurrent threads) and timeout (10 seconds) for reliable scanning
- **Data Storage:** Database schema for device inventory and scan history
- **Device Type Management:**
  - Device type creation, editing, and deletion (CRUD operations)
  - Default device types on setup: "UPS", "ATS", "PDU", "Netbotz", "Ecostruxure", "Software"
  - Device type validation: unique names, maximum 20 characters
  - Deletion warnings when device types are currently assigned to devices
  - Automatic "Unknown" device type for unassigned or deleted types (permanent, non-deleteable)
- **Security:** Rate limiting to avoid network flooding, configurable scan intensity
- **Admin Access:** All scanning functions accessible only via admin panel

**Dependencies:**
- Function #1: Multi-Level Authentication System
- Function #2: Admin Panel/Dashboard  
- Function #3: DHCP Service Management (for IP assignment correlation)

**Notes/Questions:**
- Should the scanner attempt port scanning to identify services, or just host discovery?
- Do you want integration with specific VMware vCenter/ESXi versions?
- Should there be alerting when new unknown devices appear on the network?
- What level of device fingerprinting detail do you need (OS detection, service identification)?
- Should scan results be correlated with existing device inventory if available?
- Do you need different scan profiles for different network segments?
- **VMware Credentials:** How should VMware credentials be managed?
  - Admin-configurable in admin panel?
  - Per-scan credentials or global configuration?
  - Should we support both read-only and full-access accounts?
- **VMware Security:** Should VMware API calls be logged for audit purposes?

---

### 5. Device Management System
**Priority:** High  
**Category:** Administration

**Description:**
A comprehensive device management system that organizes, categorizes, and manages all discovered network devices. This system handles device information, grouping, ownership, and presentation. It provides administrative management interfaces and handles public landing page integration for "Testdrive" devices. All management functions are admin-only and accessible through the admin panel.

**User Stories:**
- As an admin user, I want to add description labels to devices so that I can easily identify and manage them
- As an admin user, I want to assign multiple admin users as device owners so that responsibility is clearly shared and defined
- As an admin user, I want to assign devices to device groups so that I can organize devices by category or function
- As an admin user, I want to create and edit device groups with custom names so that I can organize devices according to my lab's needs
- As an admin user, I want to create device groups immediately without approval so that I can quickly organize devices as needed
- As an admin user, I want deleted device groups to automatically move devices to "Unassigned Devices" so that no devices are lost when reorganizing
- As an admin user, I want to assign multiple admin users as owners to device groups so that responsibility and identification is clearly shared
- As an admin user, I want group ownership to be optional so that not all groups require explicit ownership assignment
- As an admin user, I want all admin users to have full access to all group functionality so that ownership doesn't restrict administrative capabilities
- As an admin user, I want to receive notifications when devices are added to or removed from groups I own so that I can track changes to my assigned groups
- As an admin user, I want devices to automatically inherit ownership from their assigned group when moved so that ownership changes reflect group assignments without manual intervention
- As an admin user, I want to be notified when I become an owner of a device due to group changes so that I'm aware of new responsibilities
- As an admin user, I want to be notified when I'm removed as an owner of a device due to group changes so that I'm aware when my responsibilities change
- As an admin user, I want devices to retain their current ownership when moved to groups without owners so that ownership continuity is maintained
- As an admin user, I want existing individual device owners to be combined with group-inherited owners so that both individual and group ownership are preserved
- As an admin user, I want to move devices between groups so that I can reorganize the lab structure as needed
- As an admin user, I want to manually override device ownership for specific devices without restrictions so that I can assign custom ownership when needed
- As an admin user, I want ownership overrides to be permanent until manually changed or overwritten by group moves so that custom assignments remain stable
- As an admin user, I want group moves to overwrite manual ownership assignments so that group inheritance takes priority during reorganization
- As an admin user, I want to see a clear organization of groups and their ownership so that I understand the lab's structure
- As an admin user, I want unassigned devices to automatically appear in an "Unassigned Devices" group so that no devices are lost in the organization
- As an admin user, I want new devices to automatically be placed in "Unassigned Devices" so that they are immediately visible and can be organized later
- As an admin user, I want the "Unassigned Devices" group to remain unowned so that it serves as a neutral holding area
- As an admin user, I want the "Unassigned Devices" group visible in the main group list so that I can easily access unorganized devices
- As an admin user, I want a standard "Testdrive" group available for testing and device assignments that should be publicly accessible
- As an admin user, I want devices in the "Testdrive" group to be visible on the landing page so that they are publicly accessible to all users (unregistered, registered, and admin)
- As an admin user, I want moving devices to "Testdrive" to implicitly make them publicly visible without additional approval workflows
- As an admin user, I want VMware hosts to automatically create device groups so that VMs are logically organized under their host
- As an admin user, I want VM guests to be automatically added to their host's device group so that the virtual infrastructure is properly organized
- As an admin user, I want to assign ownership to VMware host groups so that VM ownership is inherited from the host level for identification purposes
- As an admin user, I want to organize devices by multiple criteria (function, location, department, project) so that I can create a logical lab structure
- As an admin user, I want to be warned before deleting device groups that contain devices so that I understand the impact before proceeding
- As an admin user, I want to see group statistics (device count, owner) so that I can understand group utilization
- As an admin user, I want to filter and search devices by group so that I can quickly find devices in specific categories
- As an admin user, I want to apply settings to all devices in a group so that I can efficiently manage related devices
- As an admin user, I want to receive notifications when devices are moved between groups so that I can track organizational changes
- As an admin user, I want to create device group templates so that I can quickly set up new lab configurations
- As an admin user, I want to export and import device group configurations so that I can backup and migrate lab setups
- As an admin user, I want VMware host groups to be automatically named and managed so that virtual infrastructure is clearly organized
- As an admin user, I want VM guests to be assigned to their host groups automatically while still allowing additional group memberships so that I can see host relationships and also make VMs publicly available
- As an admin user, I want VM guests without host information to be placed in a "VM Guests" fallback group so that orphaned VMs are still organized
- As an admin user, I want to assign VM guests to additional groups like "Testdrive" so that virtual machines can be made visible on the landing page
- As an admin user, I want to assign individual devices to groups carefully so that each device is properly organized without errors
- As an admin user, I want VM host ownership to take priority over other group ownership so that virtual infrastructure ownership is clearly defined
- As an admin user, I want to configure which device information fields are visible in the device management interface so that I can customize the display for my needs
- As an unregistered visitor, I want to see "Testdrive" devices sorted by type on the landing page so that I can easily find available equipment

**Acceptance Criteria:**
- [ ] Device description labels (custom text descriptions for easy identification)
- [ ] Device owner assignment (assign multiple admin users as device owners)
- [ ] Device group assignment (assign devices to custom groups)
- [ ] Single group membership for most devices (one primary group per device)
- [ ] Multiple group membership for VM guests only (host group + additional groups)
- [ ] Device group assignment UI (dropdown selection interface for simplicity)
- [ ] Individual device group assignment only (no bulk operations for careful consideration)
- [ ] No device type restrictions for group assignments (flexible organization)
- [ ] VM host ownership priority (VMware host group ownership overrides other group ownership)
- [ ] Automatic VM guest group assignment based on host-guest relationships
- [ ] VM guests with host info auto-assigned to host-specific device groups
- [ ] VM guests without host info auto-assigned to fallback "VM Guests" group
- [ ] Manual additional group assignment for VM guests (e.g., "Testdrive" visibility)
- [ ] Custom device grouping and organization (function, location, department, project, etc.)
- [ ] Device group creation and management (CRUD operations with validation)
- [ ] Device group metadata management (name only, max 20 characters with basic formatting)
- [ ] Device group creation by any admin (no approval required)
- [ ] Device group permanent deletion with automatic device reassignment
- [ ] Simple group interface (no color coding, icons, or complex visual features)
- [ ] Device group ownership assignment (optional, multiple admin users per group)
- [ ] Group ownership for visual identification only (no special permissions)
- [ ] All admin users retain full access to all group functionality regardless of ownership
- [ ] Group owner notifications when devices are added to or removed from their groups
- [ ] Device ownership inheritance from group membership (automatic, no confirmation required)
- [ ] Automatic ownership updates when devices move between groups with different owners
- [ ] Ownership change notifications for new device owners (when added due to group changes)
- [ ] Ownership removal notifications for previous owners (when removed due to group changes)
- [ ] No notifications for owners who remain unchanged during group moves
- [ ] Ownership retention when devices move to groups without owners (preserves current ownership)
- [ ] Combined ownership model: group-inherited owners + individual owners (both preserved)
- [ ] Device ownership override capability (manual ownership assignment without restrictions)
- [ ] Permanent ownership overrides (until manually changed or overwritten by group moves)
- [ ] Group move ownership priority (group inheritance overwrites manual assignments during moves)
- [ ] No warnings or notifications for ownership overrides (silent operation)
- [ ] No visual indicators for overridden device ownership (clean interface)
- [ ] Device group organization display (flat structure, no hierarchy)
- [ ] Automatic "Unassigned Devices" group for ungrouped devices (permanent, unowned, visible in main group list)
- [ ] New devices automatically placed in "Unassigned Devices" (except VM guests with host info)
- [ ] No alerts or notifications for devices remaining in "Unassigned Devices" group
- [ ] Standard "Testdrive" group for device assignments requiring public accessibility (permanent, no restrictions)
- [ ] "Testdrive" group uses standard ownership structure (optional, multiple admin owners)
- [ ] Moving devices to "Testdrive" implicitly enables public landing page visibility (no approval required)
- [ ] No device type restrictions, auto-expiration, or special permissions for "Testdrive" group
- [ ] Automatic "VM Guests" group for VMs without host information (permanent, auto-created)
- [ ] Device group validation (unique group names, deletion warnings when groups contain devices)
- [ ] Device movement between groups with automatic ownership change notifications
- [ ] Ownership change notifications (new owners notified when added, removed owners notified when removed)
- [ ] No duplicate notifications for owners who remain unchanged during group moves
- [ ] Group-based device filtering and search capabilities
- [ ] Device group statistics display (device count, owner information, last modified)
- [ ] Bulk group assignment operations (select multiple devices, assign to group)
- [ ] Group-based device operations (apply settings to all devices in group)
- [ ] Device group templates for common lab configurations
- [ ] Group import/export functionality for backup and migration
- [ ] Orphaned device handling (move to "Unassigned Devices" when group deleted)
- [ ] "Testdrive" group devices visible on public landing page
- [ ] Landing page device display sorted by device type
- [ ] Public device information display (name, type, description, basic status)
- [ ] Automatic VMware host device group creation
- [ ] VMware host group naming convention and lifecycle management
- [ ] Automatic VM guest assignment to host device groups
- [ ] VMware host group ownership and VM inheritance
- [ ] VMware group auto-maintenance (host detection, VM assignment)
- [ ] Public group display restrictions (only "Testdrive" visible to unregistered users)
- [ ] Configurable device information display (show/hide device fields)
- [ ] Admin device management interface in admin panel

**Technical Notes:**
- **Device Information Management:**
  - Device description labels (custom text for easy identification, maximum 20 characters with basic formatting support)
  - Device owner assignment (assign multiple admin users as device owners for shared responsibility)
  - Device ownership inheritance from group membership with ability to assign additional individual owners
  - Device ownership override capability:
    - Manual ownership assignment without restrictions or special permissions
    - Permanent overrides (stable until manually changed or overwritten)
    - Group moves overwrite manual assignments (group inheritance takes priority)
    - No warnings, notifications, or visual indicators for overridden ownership
    - Silent operation for clean user experience
  - Device owner assignment and contact information
  - Configurable device information display (show/hide columns/fields in device management interface)
- **Device Organization & Grouping:**
  - **Device Group Assignment:**
    - Single device group membership for most devices (one device → one primary group)
    - Multiple group membership for VM guests only (host group + additional groups like "Testdrive")
    - Admin device group assignment via dropdown selection interface (simple, reliable UI)
    - Individual device group assignment only (no bulk operations to ensure careful consideration)
    - Automatic VM guest group assignment based on host-guest relationships from Function #4
    - VM guests with known host info: auto-assign to host-specific device group
    - VM guests without host info: auto-assign to fallback "VM Guests" group (permanent, auto-created)
    - Manual additional group assignment for VM guests (e.g., add to "Testdrive" for public visibility)
    - No device type restrictions for group assignments (flexible organization)
    - VM host ownership priority: VMware host group ownership overrides other group ownership
    - Device group assignment validation and conflict checking
  - Custom device grouping capabilities (by function, location, type, department, project, etc.)
  - Device group creation, editing, and deletion (CRUD operations with validation)
  - Device group metadata: name (required, max 20 characters with basic formatting support), created date, modified date
  - Device group organization: flat structure (no hierarchy or nested groups at this time)
  - Future extensibility: group hierarchy can be added later if needed
  - Device group ownership assignment (optional, multiple admin users per group for visual identification)
  - Hierarchical ownership model: Group Owner(s) → Device inheritance (automatic, no confirmation required)
  - Individual device ownership: Group inheritance + additional individual owners (combined ownership model)
  - Automatic ownership updates when devices move between groups with different owners
  - Ownership change notification system:
    - New owners notified when added due to group changes
    - Removed owners notified when removed due to group changes  
    - No notifications for owners who remain unchanged during group moves
  - Ownership retention rules:
    - Device moved to group with owners: inherits group owners + retains individual owners
    - Device moved to group without owners: retains current ownership (no change)
    - Individual owners always preserved regardless of group changes
    - Manual ownership overrides overwritten by group moves (group inheritance priority)
  - VM ownership priority model: VMware Host Group Owner(s) → VM Device ownership (overrides other group ownership)
  - Group ownership for identification only (all admin users retain full access to all group functionality)
  - Device groups can exist without assigned owners (ownership is optional)
  - Group owner notifications when devices are added/removed from their groups
  - Automatic default groups: 
    - "Unassigned Devices" (permanent, unowned, visible in main group list, default for new devices)
    - "Testdrive" (permanent, standard ownership structure, public landing page visibility)
    - "VM Guests" (permanent, auto-created)
  - "Unassigned Devices" group behavior:
    - New devices automatically placed here (except VM guests with host info)
    - Permanent group (cannot be deleted)
    - No owner assignment (remains unowned)
    - Visible in main group list for easy access
    - No alerts or notifications for devices remaining in group
    - Serves as neutral holding area for device organization
  - Device group validation: unique group names, deletion warnings when groups contain devices
  - Device group creation: any admin can create groups immediately (no approval required)
  - Device group deletion: permanent deletion with automatic device reassignment to "Unassigned Devices"
  - Simple group interface: no color coding, icons, or complex visual organization features
  - Device group validation: unique group names, prevent deletion of groups with assigned devices
  - Device movement between groups (with ownership change notifications)
  - Group-based device filtering and search capabilities
  - Device group statistics (device count, owner information, last modified)
  - Automatic VMware host device group creation and management
  - VMware host group naming convention: "VMware Host - [hostname]" or "VMware Host - [IP]"
  - Automatic VM guest assignment to host device groups
  - VMware-specific ownership: Host Group Owner → VM Device inheritance
  - VMware group lifecycle management (auto-create when host detected, auto-maintain VM assignments)
  - Orphaned device handling (devices whose groups are deleted move to "Unassigned Devices")
  - Group import/export functionality for backup and migration
  - Device group templates for common lab configurations
  - Individual device group assignment (no bulk operations for careful consideration)
  - Group-based device operations (apply settings to all devices in group)
  - "Testdrive" group integration with public landing page for device visibility (all user types)
  - "Testdrive" group behavior:
    - Permanent group (cannot be deleted)
    - Standard ownership structure (optional, multiple admin owners)
    - No device type restrictions or special permissions
    - No auto-expiration or approval workflows
    - Moving devices to group implicitly enables public visibility
    - Accessible to all user types (unregistered, registered, admin)
  - Landing page device sorting by device type for public access
  - Public group display restrictions (only "Testdrive" group visible to unregistered users)
- **User Interface:**
  - Admin management interface in admin panel (PAM authentication required)
  - Public landing page integration for "Testdrive" devices (no authentication)
- **Data Integration:** Consumes device data from Network Device Scanner (Function #4)
- **Access Control:** Admin-only management with public "Testdrive" device display

**Dependencies:**
- Function #1: Multi-Level Authentication System
- Function #2: Admin Panel/Dashboard  
- Function #4: Network Device Scanner (for device data)

**Notes/Questions:**
- **Device Grouping:** What default device groups should be created (e.g., "Network Equipment", "Servers", "UPS/PDUs")?
- **Owner Management:** Should device owners be selected from existing users or allow free-text entry?
- **Group Ownership:** Should device group ownership be limited to admin users only, or include registered users?
- **Ownership Inheritance:** Should there be warnings when overriding group-inherited ownership?
- **Group Hierarchy:** ✅ No group hierarchy needed at this time (flat structure), can be added later if required
- **Bulk Operations:** What bulk operations should be available (move devices, change ownership, etc.)?
- **Default Groups:** Should the system create default groups on first setup?
- **Unassigned Devices Group:** ✅ Permanent group (cannot be deleted), unowned, visible in main group list, default destination for new devices
- **Testdrive Group:** ✅ Permanent group (cannot be deleted), standard ownership structure, no restrictions or approval workflows, public visibility for all user types
- **Testdrive Group Display:** Should "Testdrive" group devices show real-time status or cached information on the landing page?
- **Landing Page Refresh:** How often should the landing page device information be updated?
- **Device Information Privacy:** What level of device detail should be visible to unregistered users?
- **Device Descriptions:** Should device descriptions have character limits or formatting restrictions?
- **Device Types:** ✅ Default device types to be created on system setup: "UPS", "ATS", "PDU", "Netbotz", "Ecostruxure", "Software"
- **Device Type Deletion:** ✅ Yes, show warnings when deleting device types that are currently assigned to devices
- **Device Type Validation:** ✅ Device type names must be unique with maximum length of 20 characters
- **Unknown Device Type:** ✅ "Unknown" device type is permanent (serves as fallback for unassigned devices)
- **Device Owner Selection:** Should device owners be limited to admin users only, or include registered users?
- **VMware Auto-Grouping:** Should VMware host groups be deleteable, or always auto-maintained?
- **VM Movement:** Should VMs be moveable between host groups, or always tied to their physical host?
- **Host Group Naming:** Should VMware host groups use hostname, IP, or custom naming?
- **Orphaned VMs:** How should VMs be handled when their host is not authenticated or accessible?
- **VM Details:** How much VM detail should be displayed to regular users vs admins?
- **Device Display Configuration:** What device fields should be configurable for display (IP, MAC, hostname, type, description, owner, group, status, etc.)?
- **Default Display Settings:** What device information should be shown by default in the device management interface?

---

### 6. Dynamic Help and Feedback System
**Priority:** Medium  
**Category:** User Experience

**Description:**
A comprehensive, context-aware help system combined with integrated user feedback capabilities that provides users with relevant assistance throughout the application. The help system should be accessible from any page and provide contextual information based on the current user's role (unregistered, registered, admin) and the specific page or feature they're using. The feedback component allows users to rate help content, suggest improvements, and submit general application feedback. This system enhances user experience by providing immediate access to relevant documentation and creating a feedback loop for continuous improvement.

**User Stories:**
- As an unregistered visitor, I want to access help information about the landing page and public features so that I can understand what's available
- As a registered user, I want to see help content relevant to my user level so that I can learn how to use the tools and features available to me
- As an admin user, I want comprehensive help for administrative functions so that I can efficiently manage the system
- As any user, I want context-sensitive help that shows information relevant to the current page so that I get targeted assistance
- As any user, I want to search the help system so that I can find specific information quickly
- As any user, I want help content to be clearly organized by topic and user role so that I can navigate to relevant sections easily
- As any user, I want visual indicators (tooltips, help icons) on complex features so that I can get instant clarification
- As any user, I want help content to include examples and step-by-step instructions so that I can better understand how to use application features
- As an admin user, I want help content for troubleshooting common application issues so that I can resolve problems quickly
- As an admin user, I want to edit help content through the admin panel so that I can maintain and update documentation as needed
- As any user, I want to rate help content as helpful or not helpful so that the system can improve over time
- As any user, I want to suggest improvements to help content so that documentation stays current and useful
- As a registered user, I want to submit general feedback about the application so that I can contribute to system improvements
- As a registered user, I want to report issues or bugs through the feedback system so that problems can be addressed
- As an admin user, I want to view and manage user feedback through the admin panel so that I can respond to user needs and track suggestions
- As an admin user, I want to see feedback analytics and trends so that I can identify common issues and improvement opportunities
- As an admin user, I want to respond to user feedback and mark issues as resolved so that users know their input is valued and addressed
- As a registered user, I want to view the status and responses to my submitted feedback through the application so that I can see how my input is being addressed

**Acceptance Criteria:**
- [ ] Global help access (help button/icon available on all pages)
- [ ] Context-aware help content (different help based on current page/section)
- [ ] Role-based help filtering (content appropriate for user's authentication level)
- [ ] Help content organization by topics and user roles:
  - [ ] Landing page and public features (all users)
  - [ ] Device monitoring and tools (registered users)
  - [ ] Administrative functions (admin users only)
  - [ ] System management and troubleshooting (admin users only)
- [ ] Search functionality within help system
- [ ] Help content categories:
  - [ ] Getting started guides for each user role
  - [ ] Application feature documentation
  - [ ] Troubleshooting guides for application issues
  - [ ] FAQ section for common questions
  - [ ] System requirements and technical information
- [ ] Interactive help elements:
  - [ ] Tooltips on form fields and complex interface elements
  - [ ] Help icons next to important features
  - [ ] Contextual help panels that can be toggled on/off
- [ ] Help content includes:
  - [ ] Step-by-step instructions for application features
  - [ ] Screenshots and visual examples
  - [ ] Common error messages and solutions
  - [ ] Feature usage examples and best practices
- [ ] Admin content management:
  - [ ] Rich text editor with Markdown support in admin panel
  - [ ] Content organization by categories and user roles
  - [ ] Content publishing workflow (draft, review, publish)
  - [ ] Version control for help content changes
  - [ ] Content preview and validation functionality
- [ ] Help system navigation:
  - [ ] Table of contents with expandable sections
  - [ ] Breadcrumb navigation within help content
  - [ ] "Related topics" suggestions
  - [ ] Recent help topics accessed by user
- [ ] Responsive help interface (works on desktop, tablet, mobile)
- [ ] Help content versioning (track updates and changes)
- [ ] User feedback mechanism for help content (helpful/not helpful ratings)
- [ ] Feedback system features:
  - [ ] Help content rating system (thumbs up/down or 5-star rating)
  - [ ] Feedback submission form for registered users
  - [ ] General application feedback and suggestions
  - [ ] Bug reporting capability with structured forms
  - [ ] Anonymous feedback option for unregistered users on help content only
  - [ ] Feedback categorization (bug report, feature request, general feedback, help improvement)
- [ ] Admin feedback management:
  - [ ] Feedback dashboard in admin panel showing all submitted feedback
  - [ ] Feedback filtering and search (by type, date, user, status)
  - [ ] Admin response system (reply to user feedback)
  - [ ] Feedback status tracking (new, in progress, resolved, closed)
  - [ ] Feedback analytics and reporting (common issues, satisfaction trends)
  - [ ] Bulk feedback operations (mark resolved, assign categories)
- [ ] User feedback experience:
  - [ ] Feedback envelope icon (✉) in navigation bar for easy access
  - [ ] Red notification dot on envelope icon when admin has replied to user's feedback
  - [ ] Confirmation messages when feedback is submitted
  - [ ] In-app notifications when admins respond to user feedback
  - [ ] Simple feedback forms integrated into relevant application pages
  - [ ] Feedback access for all user types (unregistered users: anonymous feedback only)
  - [ ] Red notification badge clears when user views admin response

**Technical Notes:**
- **Content Management:** 
  - Markdown-based help content for easy editing and version control
  - Admin content editor in admin panel for web-based help content management
  - Content categorization system with tags for role, topic, and feature area
  - Help content stored in database with caching for performance
  - Version control for help content changes (track edits, restore previous versions)
  - Content validation and preview functionality in admin editor
- **Admin Content Editor:**
  - Rich text editor with Markdown support and live preview
  - Content organization by categories, topics, and user roles
  - Drag-and-drop content organization and hierarchy management
  - Content publishing workflow (draft → review → publish)
  - Bulk content operations (import, export, backup)
- **Context Detection:**
  - URL-based context awareness (different help for different pages)
  - JavaScript integration to detect current page section and user role
  - Dynamic content loading based on context
- **Search Implementation:**
  - Full-text search across all help content
  - Search result ranking based on user role and current context
  - Search suggestions and auto-complete functionality
- **User Interface:**
  - Modal dialogs or slide-out panels for help content display
  - Overlay system for contextual tooltips and hints
  - Responsive design for various screen sizes
- **Content Delivery:**
  - Static content caching for performance
  - Progressive loading of help content to minimize initial page load
  - Application-focused content scope (features, usage, troubleshooting)
- **Analytics:**
  - Track help content usage to identify most accessed topics
  - Monitor search queries to identify content gaps
  - User feedback collection and analysis
- **Feedback System Implementation:**
  - **Database Schema:**
    - Feedback table with user ID, content type, rating, comments, timestamp
    - Feedback categories and status tracking
    - Admin response tracking with timestamps
  - **User Experience:**
    - Simple rating widgets (thumbs up/down or star ratings) embedded in help content
    - Feedback forms accessible from help pages and main application areas
    - Confirmation messages and in-app notifications for feedback acknowledgment
  - **Admin Interface:**
    - Feedback dashboard showing submission trends and common issues
    - Filtering and search capabilities for feedback management
    - Response system for direct user communication
    - Analytics dashboard showing satisfaction trends and improvement areas
  - **Integration:**
    - Help content rating integration for continuous improvement
    - Context-aware feedback forms (page-specific feedback)
    - In-app notification system for feedback responses

**Dependencies:**
- Function #1: Multi-Level Authentication System (for role-based content)
- Function #2: Admin Panel/Dashboard (for admin-specific help content)

**Notes/Questions:**
- **Offline Capability:** Should critical help content be available offline or is online-only acceptable?
- **Integration Level:** Should help be fully integrated into the application or can it be a separate help site/system?
- **Localization:** Will the application need multi-language support for help content?
- **User-Generated Content:** Should users be able to contribute to help content or suggest improvements?
- **Feedback Integration:** Should feedback be integrated with existing ticketing systems or remain self-contained?
- **Feedback Moderation:** Should user feedback require admin approval before being visible, or should it be immediately available?
- **Feedback Analytics:** What specific metrics should be tracked for feedback analysis (response time, resolution rate, satisfaction scores)?
- **Feedback Anonymity:** Should users be able to submit anonymous feedback, or require authentication for all feedback?
- **Feedback Export:** Should admins be able to export feedback data for external analysis or reporting?
- **In-App Notifications:** Should the system use browser notifications, dashboard alerts, or simple status indicators for feedback responses?

---

### 7. Landing Page and Public Interface
**Priority:** High  
**Category:** User Experience

**Description:**
The public-facing landing page serves as the main entry point to the Lab Portal Management System. This page provides the foundational structure, navigation, and basic information display that all users see regardless of their authentication status. The landing page adapts its content and navigation based on the user's authentication level while maintaining a consistent, professional appearance.

**User Stories:**
- As any visitor, I want to see a professional, welcoming landing page so that I understand this is a legitimate lab portal
- As any visitor, I want the page to load quickly so that I can access it efficiently
- As any visitor, I want clear navigation options appropriate to my authentication level so that I can access the features available to me
- As any visitor, I want to see basic lab information so that I understand the purpose and scope of this portal
- As an unregistered visitor, I want clear options to register or log in so that I can access additional features
- As a registered user, I want to see my login status and appropriate navigation so that I know I'm authenticated and can access my features
- As an admin user, I want quick access to the admin panel so that I can manage the system efficiently

**Acceptance Criteria:**
- [ ] Clean, professional landing page design accessible without authentication
- [ ] Desktop-focused design optimized for standard desktop browsers
- [ ] Fast loading performance (under 3 seconds initial load)
- [ ] Basic lab information section:
  - [ ] Lab logo and editable text display (top left corner positioning)
  - [ ] Admin-editable logo upload and text field (admin users only)
  - [ ] "Testdrive" device group overview (list/summary of available devices sorted by device type)
  - [ ] Admin-configurable "Important Info" banner (appears below navigation bar when content exists)
  - [ ] No mission statement, contact details, or operating hours required
- [ ] Dynamic navigation based on user authentication status:
  - [ ] Unregistered users: Login, Register, ✉, ?
  - [ ] Registered users: Home, Tools, Welcome message, Logout, ✉, ?
  - [ ] Admin users: Home, Tools, Admin Panel, Welcome message, Logout, ?
- [ ] Authentication status indicator:
  - [ ] Clear indication when user is logged in
  - [ ] Simple "Welcome, [Username]" text with logout link
- [ ] Content management integration:
  - [ ] Admin-editable logo upload and text field functionality
  - [ ] Logo optimization (compression, format conversion if not complex to implement)
  - [ ] Optional logo preview system (if not complex to implement)
  - [ ] Rich text "Important Info" banner editor (appears below navigation when content exists)
  - [ ] Content publishing workflow (draft → publish action required)
  - [ ] Content change tracking and audit log (accessible via admin panel)
  - [ ] Simple content revert capability (revert to previous version, not full version history)
  - [ ] Real-time "Testdrive" device list integration from Function #5
  - [ ] Admin-configurable device information display for public landing page
  - [ ] Real-time content updates without page refresh
- [ ] Technical requirements:
  - [ ] WCAG 2.1 compliance for accessibility
  - [ ] Search engine optimization (basic SEO)
  - [ ] Progressive enhancement for older browsers
  - [ ] Semantic HTML structure for accessibility
- [ ] Navigation framework:
  - [ ] Role-based menu system with simple horizontal navigation bar
  - [ ] Help icon (?) positioned in top-right corner, always visible
  - [ ] Simple "Welcome, [Username]" text for authenticated users
  - [ ] Prominent "Admin Panel" link for admin users
  - [ ] No footer - minimal design approach

**Technical Notes:**
- **Frontend Framework:**
  - Modern CSS framework (Bootstrap, Tailwind, or similar) 
  - Desktop-focused design approach optimized for standard desktop browsers
  - Semantic HTML5 structure for accessibility and SEO
- **Authentication Integration:**
  - Session detection and user role identification
  - Dynamic content loading based on authentication status
  - Secure session management integration
- **Content Management:**
  - **Logo Management:**
    - Admin-editable logo upload (PNG, SVG, JPG formats, max 2MB)
    - Automatic logo optimization (compression, format conversion if implementation complexity is reasonable)
    - Optional preview system for logo changes (if implementation complexity is reasonable)
    - Fixed 64x64px container with responsive scaling for different logo aspect ratios
  - **Text Content Management:**
    - Simple text field for lab name/title next to logo (basic formatting support)
    - Rich text "Important Info" banner editor (supports bold, italic, links)
    - Banner only displays when content exists (hidden when empty)
    - Content publishing workflow (draft → publish action required for all changes)
  - **Content Change Management:**
    - Change tracking and audit log for all content modifications
    - Track: admin user, timestamp, content type, change description
    - Audit log accessible via admin panel interface
    - Simple revert capability (revert to previous version only, no full version history)
    - Any admin user can make content changes (no approval workflow)
  - **Device Display Integration:**
    - Automatic "Testdrive" device group integration for equipment overview display
    - Admin-configurable device information visibility for public landing page
    - Admin controls which device fields are displayed to unregistered users
    - Device information sourced from Function #5 (Device Management System)
    - No separate device description editing (uses scanner-detected information)
  - Content caching for performance optimization
- **Performance Optimization:**
  - Static asset optimization and compression
  - Content delivery optimization for fast loading
  - Lazy loading for non-critical content
- **Accessibility and SEO:**
  - WCAG 2.1 AA compliance for accessibility
  - Meta tags and structured data for search engines
  - Alt text for images and proper heading hierarchy
  - ARIA labels for screen readers

**Dependencies:**
- Function #1: Multi-Level Authentication System (for user status detection and role-based navigation)
- Function #5: Device Management System (for "Testdrive" device data and admin-configurable device information display)

**Logo and Branding Requirements:**
- **Logo Upload:** Support PNG, SVG, and JPG formats for maximum flexibility
- **Logo Sizing:** Hybrid approach - fixed square container (64x64px) with dynamic scaling:
  - Square logos: Display at full 64x64px size for crisp appearance
  - Non-square logos: Auto-scale to fit within 64x64px container while maintaining aspect ratio
  - Recommended: Square logos for optimal professional appearance
- **Logo Management:**
  - Logo optimization: Automatic compression and format conversion (if implementation complexity is reasonable)
  - Preview system: Optional preview before publishing logo changes (if implementation complexity is reasonable)
  - No logo versioning required (simple replacement system)
- **Logo Text:** Admin-editable text field displayed next to logo (lab name, organization, etc.)
- **Admin Management:** Logo upload and text editing accessible only to admin users via admin panel
- **Technical Specifications:**
  - Logo container: Fixed 64x64px square for consistent layout
  - Supported formats: PNG (recommended), SVG, JPG
  - Maximum file size: 2MB for performance
  - Text field: Maximum 50 characters with basic formatting support
- **Content Management Features:**
  - **Important Info Banner:**
    - Rich text editor with support for bold, italic, links
    - Appears below navigation bar when content exists
    - Hidden when content field is empty
    - Visible to all user types (unregistered, registered, admin)
  - **Publishing Workflow:**
    - All content changes require publish action (no immediate updates)
    - Draft → Publish workflow for both logo and text content
  - **Change Tracking:**
    - Audit log for all content modifications (admin user, timestamp, change type)
    - Accessible via admin panel interface
    - Simple revert capability (revert to previous version, no full history)
  - **Device Information Display:**
    - Admin-configurable device information visibility for "Testdrive" devices on landing page
    - Admins control which device fields are displayed to public users
    - Uses scanner-detected information from Function #5 (no separate editing)
- **Implementation Notes:**
  - Logo optimization and preview features should be implemented only if complexity is reasonable
  - Any admin user can make content changes (no approval workflow required)
  - No export/import capabilities required for content
  - No full version history required (simple revert to previous version only)

---

### 8. Unregistered User Features
**Priority:** High  
**Category:** User Experience

**Description:**
Features and capabilities available to visitors who have not registered or logged into the system. These features provide immediate value to potential users while encouraging registration for additional functionality. The focus is on showcasing publicly available resources and providing easy access to registration and help systems.

**User Stories:**
- As an unregistered visitor, I want to view publicly available equipment without logging in so that I can see what's accessible for testing
- As an unregistered visitor, I want to see "Testdrive" devices organized by type so that I can easily find equipment I'm interested in
- As an unregistered visitor, I want to see basic device information and status so that I can understand what each device offers and its availability
- As an unregistered visitor, I want to access help information so that I can learn about the lab and its services
- As an unregistered visitor, I want to register for an account so that I can access additional features
- As an unregistered visitor, I want to see device status updates so that I know current availability
- As an unregistered visitor, I want clear information about what additional features are available to registered users so that I understand the benefits of registration
- As an unregistered visitor, I want to search or filter public devices so that I can quickly find specific types of equipment

**Acceptance Criteria:**
- [ ] "Testdrive" device display on landing page for all users (including unregistered)
- [ ] Device information displayed: name, type, description, status (basic info only)
- [ ] Information security: No sensitive technical details exposed (IP addresses, credentials, management interfaces hidden)
- [ ] Device display managed from admin interface (admin control over public visibility)
- [ ] Device interaction capabilities:
  - [ ] Device status indicator (visual status representation)
- [ ] Real-time device status updates:
  - [ ] Automatic refresh: Device status updates every 5 minutes (configurable interval)
  - [ ] Live status updates: Real-time status changes without requiring page reload
  - [ ] Status types available:
    - [ ] Online: Device is responding and available
    - [ ] Offline: Device is not responding or powered down
  - [ ] Performance optimization: Device information cached for fast loading while maintaining current status
- [ ] User registration and account creation:
  - [ ] User registration form with proper validation
  - [ ] Required information fields: Username (unique validation), Email address (format validation only), Password, Confirm password
  - [ ] Password requirements: 8 character minimum, 32 character maximum
  - [ ] No email verification process required (format validation only for admin contact purposes)
- [ ] Help and information access:
  - [ ] Access to public help content from Dynamic Help System
  - [ ] Getting started guide potentially integrated into help menu
- [ ] User experience features:
  - [ ] Clear call-to-action for registration
  - [ ] Feature comparison (unregistered vs registered capabilities)
  - [ ] Smooth navigation between public features

**Technical Notes:**
- **Device Data Integration:**
  - Real-time device data from Function #5 (Device Management System)
  - Query "Testdrive" group devices with status filtering
  - Device status API integration for live updates
  - Data caching with configurable refresh intervals
- **Security and Privacy:**
  - Limited device information exposure (no IP addresses or technical specs)
  - No authentication required for public features
  - Rate limiting for search and filtering to prevent abuse
- **Registration System:**
  - Secure user registration with email verification
  - Password strength requirements and validation
  - Account creation workflow integration with Function #1
- **Performance Optimization:**
  - Device data caching to minimize database load
  - Lazy loading for device images and detailed information
  - Search optimization for fast device filtering
- **Help System Integration:**
  - Integration with Function #6 (Dynamic Help System)
  - Context-aware help content for unregistered users
  - Public help content filtering and display

**Dependencies:**
- Function #1: Multi-Level Authentication System (for registration functionality)
- Function #5: Device Management System (for "Testdrive" device data)
- Function #6: Dynamic Help System (for public help content)
- Function #7: Landing Page and Public Interface (for basic page structure)

**Notes/Questions:**
- **Device Information Scope:** What level of device detail should be visible to unregistered users?
- **Registration Requirements:** What information should be required for user registration (email, name, affiliation)?
- **Device Status Types:** What status options should be displayed (Available, In Use, Offline, Maintenance)?
- **Search Capabilities:** Should search include device descriptions, or just names and types?
- **Registration Benefits:** What specific features should be highlighted as benefits of registration?
- **Contact Integration:** Should contact forms be available to unregistered users?

---

### 9. Registered User Features
**Priority:** High  
**Category:** User Experience

**Description:**
Features and capabilities available to users who have registered and authenticated with database credentials. Registered users get the same access as unregistered users plus the ability to provide feedback to admins, access to a "Tools" menu (to be specified later), and basic profile management capabilities.

**User Stories:**
- As a registered user, I want to submit feedback about the application so that I can contribute to system improvements and communicate with admins
- As a registered user, I want to receive replies from admins to my feedback so that I can see responses to my input
- As a registered user, I want to access a "Tools" menu so that I can use additional functionality not available to unregistered users
- As a registered user, I want to change my password so that I can maintain account security
- As a registered user, I want to delete my profile so that I can remove my account when no longer needed
- As a registered user, I want to access the same help content as unregistered users so that I can get assistance with the application

**Acceptance Criteria:**
- [ ] Same landing page access as unregistered users:
  - [ ] View "Testdrive" device display with basic information
  - [ ] Device status indicators (online/offline)
  - [ ] Real-time device status updates (5-minute intervals)
- [ ] Enhanced navigation:
  - [ ] Navigation shows: Home, Tools, Welcome message, Logout, ✉, ?
  - [ ] Access to "Tools" menu (functionality to be specified later)
  - [ ] Feedback envelope icon (✉) in navigation bar
- [ ] Feedback system capabilities:
  - [ ] Submit general application feedback and suggestions
  - [ ] Bug reporting capability with structured forms
  - [ ] View admin replies to submitted feedback
  - [ ] Red notification dot on envelope icon when admin has replied
  - [ ] Red notification badge clears when user views admin response
  - [ ] Feedback categorization (bug report, feature request, general feedback)
- [ ] Basic profile management:
  - [ ] Change password functionality with validation
  - [ ] Delete profile/account capability
  - [ ] Profile deletion includes all user data and feedback history
- [ ] Help system access:
  - [ ] Access to same help content as unregistered users
  - [ ] No additional registered-user-specific help content required

**Technical Notes:**
- **Authentication and Authorization:**
  - Database authentication verification for registered user features
  - Session management and timeout handling
  - Role-based access control distinguishing registered users from admins
- **Landing Page Access:**
  - Same device viewing capabilities as unregistered users
  - Access to "Testdrive" group devices with basic information
  - Real-time device status updates (online/offline status)
- **Feedback System Integration:**
  - Integration with Function #6 (Dynamic Help and Feedback System)
  - Feedback submission, tracking, and admin response system
  - In-app notification system for admin responses
- **Tools Menu:**
  - Navigation framework for future tools functionality
  - Placeholder for tools to be specified later
  - Secured access restricted to registered users only
- **Profile Management:**
  - Secure password change functionality with validation
  - Account deletion capability with complete data cleanup
  - User data privacy and removal compliance
- **Security:**
  - All registered user functions require database authentication
  - Session security and logout capabilities
  - No access to admin functions or enhanced device information

**Dependencies:**
- Function #1: Multi-Level Authentication System (for registered user authentication)
- Function #6: Dynamic Help System (for feedback functionality)
- Function #7: Landing Page and Public Interface (for navigation framework)

**Notes/Questions:**
- **Tools Menu Content:** What specific tools should be included in the Tools menu?
- **Profile Deletion:** Should account deletion be immediate or have a grace period?
- **Feedback Categories:** Are the basic feedback categories (bug report, feature request, general feedback) sufficient?
- **Password Requirements:** Should password change require current password verification?
- **Data Retention:** How long should deleted user feedback be retained for admin reference?

---

### 10. Device Interaction Tools
**Priority:** Medium  
**Category:** User Experience

**Description:**
A comprehensive tools interface accessible to registered users for interacting with devices in the "Testdrive" group. This function provides three distinct tools that enable registered users to monitor, control, and interact with lab devices that have been made publicly accessible. Each tool is designed for specific device interaction scenarios and provides registered users with enhanced capabilities beyond basic device browsing.

**User Stories:**
- As a registered user, I want to access a Tools menu so that I can interact with Testdrive devices using specialized tools
- As a registered user, I want to see all three device interaction tools in one organized interface so that I can choose the appropriate tool for my needs
- As a registered user, I want each tool to have clear descriptions and usage instructions so that I understand when and how to use each tool
- As a registered user, I want the tools to work only with Testdrive devices so that I have appropriate access levels
- As a registered user, I want tools to be responsive and provide feedback so that I know when actions are successful or failed
- As a registered user, I want to switch between tools easily so that I can use multiple tools during my lab session
- As a registered user, I want tools to remember my recent interactions so that I can quickly access previously used devices
- As a registered user, I want tools to show device availability status so that I know which devices are ready for interaction
- As a registered user, I want error messages and troubleshooting guidance when tools fail so that I can resolve issues independently

**Acceptance Criteria:**
- [ ] Tools menu accessible only to registered users (authentication required)
- [ ] Three distinct tool subsections with clear navigation between them
- [ ] Device filtering to show only "Testdrive" group devices in all tools
- [ ] Consistent tool interface design and user experience across all three tools
- [ ] Real-time device status indicators for availability and responsiveness
- [ ] Error handling and user feedback for all tool operations
- [ ] Tool usage logging for troubleshooting and analytics
- [ ] Help integration for each tool with context-sensitive documentation
- [ ] Recent device interaction history for quick access
- [ ] Device compatibility indicators showing which tools work with each device type

**Tool 1: SNMP Browser & Management Tool**
- [ ] Browse and explore SNMP MIB trees for devices that support SNMP
- [ ] Search MIB objects by name, OID, or description for quick navigation
- [ ] Display SNMP object values (strings, integers, counters, etc.) with automatic formatting
- [ ] SNMP table browsing with tabular display for multi-instance objects
- [ ] User interface with simplified SNMP version selection (v1, v3) with automatic v2c optimization
- [ ] SNMP v1/v2c authentication using community strings with configurable defaults ("public", "private", "community")
- [ ] SNMP v3 authentication with configurable security options (basic: MD5/SHA + DES/AES, full: admin-enabled)
- [ ] Dual OID input methods: text input with MIB-based autocomplete AND interactive MIB tree browser
- [ ] MIB library management with always-loaded system MIBs and optional user-uploaded MIBs per session
- [ ] Session-only credential storage (no database persistence) for enhanced security
- [ ] Export SNMP data in multiple formats (CSV, JSON, text) for external analysis
- [ ] Real-time value monitoring with configurable refresh intervals
- [ ] Session-based command history and bookmarking for frequently accessed OIDs
- [ ] Admin configuration interface for default community strings per device and SNMPv3 protocol complexity
- [ ] Error handling for unreachable devices or invalid SNMP requests
- [ ] Integration with device scanner data to show SNMP-capable devices

**Tool 2: Modbus TCP Client**
- [ ] Connect to Modbus TCP devices on standard port 502 with basic timeout settings
- [ ] Support for standard Modbus function codes for reading data (read coils, discrete inputs, holding registers, input registers)
- [ ] Manual register address input with support for single register or range reading
- [ ] Basic data type interpretation (16-bit integers, 32-bit integers, floating point, raw hex values)
- [ ] Simple register value display with manual refresh capability
- [ ] Device connection testing to verify Modbus TCP connectivity
- [ ] Register read history within current session for easy re-access
- [ ] Export register values for current session (CSV, text format)
- [ ] Basic error handling for connection failures and invalid register addresses
- [ ] Integration with device scanner to identify Modbus TCP capable devices
- [ ] Simple tabbed interface for multiple device connections
- [ ] Address format support (decimal, hexadecimal input for register addresses)

**Tool 3: Network Probing Tool (Embedded Nmap)**
- [ ] Embedded nmap functionality exclusively for "Testdrive" group devices
- [ ] Admin-manageable scan script library with CRUD operations in admin panel
- [ ] Device target selection restricted to "Testdrive" group devices only
- [ ] Predefined scan scripts with hardcoded nmap parameters and target IP injection
- [ ] Initial scan scripts:
  - [ ] SSL Cipher Enumeration: `nmap -sV --script ssl-enum-ciphers -p 443 [target_ip]`
  - [ ] SSH Algorithm Enumeration: `nmap --script ssh2-enum-algos [target_ip]`
- [ ] Scan result display with formatted output (script results, service information)
- [ ] Scan history and result storage for current user session
- [ ] Export scan results in multiple formats (XML, JSON, text, CSV)
- [ ] Real-time scan progress indication and cancellation capability
- [ ] Admin script management: add, edit, delete, and test scan scripts
- [ ] Script validation and security checks for admin-added scripts
- [ ] Integration with device scanner data to show available "Testdrive" devices

**Technical Notes:**
- **Access Control:**
  - Registered user authentication required for all tools
  - Tools restricted to "Testdrive" group devices only
  - Role validation on every tool access and device interaction
- **Tool Framework:**
  - Modular tool architecture for easy addition of new tools
  - Consistent API interface for device interactions
  - Shared authentication and device filtering across all tools
  - Common error handling and logging framework
- **Device Integration:**
  - Integration with Device Management System (Function #5) for device data
  - Real-time device status checking before tool operations
  - Device type compatibility matrix for tool availability
  - Graceful handling of offline or unresponsive devices
- **User Experience:**
  - Responsive web interface optimized for desktop use
  - Progressive loading for tool initialization
  - Session management for tool state persistence
  - Recent device history storage (browser session-based)
- **Tool-Specific Implementation:**
  - **Tool 1 (SNMP Browser):**
    - net-snmp command-line tools integration for reliable SNMP operations
    - Simplified user interface: SNMP version dropdown showing v1 and v3 options only
    - Backend implementation: automatically use SNMPv2c when user selects v1 for better performance
    - SNMP v1 interface: Device selection, community string input (defaults: "public", "private", "community"), OID input with dual methods
    - SNMP v3 interface: Username, security level, auth/privacy protocols (simple: MD5/SHA + DES/AES, full protocols admin-configurable)
    - OID input methods: Text input with MIB-based autocomplete AND interactive MIB tree browser
    - MIB management: System MIBs always loaded (IF-MIB, SNMPv2-MIB, etc.), user MIBs optionally loaded per session
    - Session-only credential storage (no database persistence for security)
    - Admin configuration: Default community strings per device, SNMPv3 protocol complexity settings
    - Real-time polling with configurable intervals and bulk operations support
  - **Tool 2 (Modbus TCP Client):**
    - Python Modbus library integration (pymodbus or similar) for basic protocol communication
    - Simple connection management for device connectivity testing
    - Basic data type conversion for common register formats (int16, int32, float, hex)
    - Session-based command history for register addresses within current user session
    - Simple export functionality for register values (CSV, text formats)
    - Integration with device scanner data to identify Modbus TCP capable devices
    - Basic error handling and user feedback for connection and read failures
  - **Tool 3 (Network Probing Tool):**
    - Python-nmap library integration for embedded nmap functionality
    - Exclusive access to "Testdrive" group devices (target validation and filtering)
    - Admin-manageable scan script library with database storage:
      - Script name, description, nmap command template
      - Target IP placeholder injection: `[target_ip]` replaced with selected device IP
      - Admin CRUD operations: create, read, update, delete scan scripts
      - Script validation and security checks for admin-added scripts
    - Initial predefined scan scripts:
      - **SSL Cipher Enumeration:** `nmap -sV --script ssl-enum-ciphers -p 443 [target_ip]`
      - **SSH Algorithm Enumeration:** `nmap --script ssh2-enum-algos [target_ip]`
    - Script execution with automatic IP injection for selected "Testdrive" device
    - Target device selection interface showing only "Testdrive" group devices
    - Real-time scan execution with progress tracking and cancellation
    - Scan result parsing and formatted display (script output, service detection)
    - Session-based scan history storage and result retrieval
    - Export functionality for scan results (XML, JSON, text, CSV formats)
    - Admin script management interface in admin panel for script library maintenance
- **Performance:**
  - Tool loading optimized for quick access
  - Device communication timeout handling
  - Background status checking without blocking UI
  - Efficient resource usage for concurrent tool sessions
- **Admin Panel Integration - Centralized Tools Management:**
  - **Tools Management Section:** Dedicated admin panel section consolidating all device interaction tool configuration
  - **SNMP Configuration Management:**
    - Default community strings per device (global and device-specific overrides)
    - SNMPv3 protocol complexity settings (simple vs full protocol support)
    - MIB library management (upload, validate, organize system and custom MIBs)
    - SNMP version display preferences (show v1/v3 to users, backend v2c optimization)
    - Device SNMP capability detection and configuration validation
  - **Modbus Configuration Management:**
    - Modbus TCP connection settings and timeout configurations
    - Device Modbus capability detection and validation
    - Default register mapping and data type interpretation settings
    - Connection rate limiting and concurrent connection management
  - **Network Probing Script Management:**
    - Scan script library CRUD operations (create, read, update, delete)
    - Script template management with `[target_ip]` placeholder validation
    - Script security validation and testing interface
    - Predefined script management (SSL cipher enumeration, SSH algorithm enumeration)
    - Script execution monitoring and error tracking
  - **Tool Usage Analytics:**
    - Per-user tool usage statistics (frequency, session duration, error rates)
    - Tool popularity metrics and performance monitoring
    - Device interaction patterns and success rates
    - Error analysis and troubleshooting support
    - Session timeout and activity tracking across all tools
  - **Unified Tool Configuration:**
    - Centralized device compatibility matrix management
    - Global timeout and rate limiting settings for all tools
    - Tool availability controls and maintenance mode settings
    - Integrated help content management for tool-specific documentation
    - Cross-tool security policies and access control settings

**Dependencies:**
- Function #1: Multi-Level Authentication System (for registered user access)
- Function #5: Device Management System (for "Testdrive" device data)
- Function #6: Dynamic Help and Feedback System (for tool documentation)
- Function #9: Registered User Features (for navigation framework)

**Notes/Questions:**
- **Device Compatibility:** ✅ All tools work with all device types (flexible device support without restrictions)
- **Concurrent Usage:** ✅ Multiple users allowed (read-only operations don't conflict)
- **Session Management:** ✅ 30-minute timeout with warning after 25 minutes of inactivity
- **Usage Analytics:** ✅ Track tool usage per user for admin panel analytics (usage frequency, session duration, error rates)
- **Tool Access Logging:** ✅ Log tool operations for troubleshooting and audit purposes
- **SNMP Credentials:** ✅ Option A: Users enter SNMP credentials each session (more secure, no credential storage)
- **SNMP Version Strategy:** ✅ User interface shows v1 and v3 options only, with v2c used automatically in backend when v1 is selected for better error handling and bulk operations
- **SNMP Implementation:** ✅ Use net-snmp command-line tools for maximum reliability and protocol compliance
- **Community Strings:** ✅ Default community strings: "public", "private", "community" with user override capability
- **Admin Community String Config:** ✅ Admins can configure default community strings per device through admin panel
- **SNMP v3 Scope:** ✅ Simple support (MD5/SHA auth, DES/AES privacy) with admin option to enable full protocol support (SHA-256, AES-256, etc.)
- **MIB Management:** ✅ System MIBs (IF-MIB, SNMPv2-MIB, etc.) always pre-loaded; user-uploaded MIBs available for optional loading per session
- **OID Input:** ✅ Both text input with MIB-based autocomplete AND MIB tree browser (click to select) available
- **Credential Storage:** ✅ Session-only credentials for security (no database storage of SNMP credentials)
- **Modbus Access:** ✅ Available to all registered users (same access level as SNMP tools)
- **Modbus Connection Limits:** ✅ Limit to one concurrent Modbus connection per user
- **Session Data:** ✅ Session-only data storage (matches SNMP credential approach for consistency)
- **Address Formats:** ✅ Support both 0-based and 1-based addressing with user selection option
- **Performance Limitations:** ✅ 10 operations per minute per user rate limiting to prevent network flooding
- **Tool Integration:** ✅ Keep tools independent initially (no data sharing between SNMP and Modbus tools)
- **Network Probing Security:** ✅ Template-only approach with hardcoded scan parameters prevents security risks, target validation for "Testdrive" devices only

---

## Template for New Functions

Copy this template for each new function:

```markdown
### [Function Number]. [Function Name]
**Priority:** [High/Medium/Low]  
**Category:** [Category]

**Description:**
[What does this function do?]

**User Stories:**
- As a [user type], I want to [action] so that [benefit]

**Acceptance Criteria:**
- [ ] What must be true for this function to be considered complete?

**Technical Notes:**
[Any technical considerations, APIs needed, data structures, etc.]

**Dependencies:**
[What other functions must exist first?]

**Notes/Questions:**
[Any questions or clarifications needed]
```

---

## Categories for Organization

Suggested categories to help organize functions:
- **User Management** (authentication, roles, profiles)
- **Equipment Management** (inventory, booking, maintenance)
- **Scheduling** (calendar, reservations, availability)
- **Laboratory Management** (lab spaces, access control)
- **Reporting** (usage reports, analytics, exports)
- **Administration** (system settings, user management)
- **Integration** (external systems, APIs)
- **Notifications** (alerts, reminders, communications)

---

## Development Phases

Once all functions are documented, we'll organize them into development phases:

### Phase 1: Core Foundation
[Functions needed for basic system operation]

### Phase 2: Essential Features
[Primary user-facing features]

### Phase 3: Advanced Features
[Nice-to-have and advanced functionality]

### Phase 4: Integration & Polish
[Integrations, optimizations, and final features]

---

## Notes for Discussion

**Lab Context:**
- **Lab Type:** Small IT Laboratory
- **Devices:** UPS units (network mgmt cards), PDUs (network interface), NetBotz environmental monitoring, VM servers with complex applications
- **VMware Environment:** 
  - One vCenter Server managing one ESXi host
  - One standalone ESXi host (direct management)
- **Primary Users:** IT professionals, system administrators, lab users
- **Security Model:** Hybrid authentication (PAM + database)

**Technical Environment:**
- **Platform:** Web Application (Browser-based)
- **Server OS:** Rocky Linux 9.6 (RHEL-compatible, LTS)
- **Deployment:** Self-hosted on Linux server
- **Architecture:** Client-server web application
- **DHCP Server:** ISC KEA DHCP (with REST API integration)

**Technology Stack Requirements:**
- **DHCP Service:** ISC KEA DHCP v2.x
  - REST API for web integration
  - JSON configuration format
  - Available via EPEL repository on Rocky Linux
  - Modern, actively maintained alternative to ISC DHCP
- **Authentication:** PAM Integration
  - Python PAM library (python-pam or similar)
  - System-level authentication for admin users
  - Required for DHCP management and other system operations
- **Privilege Management:** 
  - Sudo configuration for web application service account
  - Secure privilege escalation for system operations
- **Network Scanning:**
  - Nmap for network discovery and device fingerprinting
  - Python-nmap library for programmatic access
  - Background task processing (Celery/Redis or APScheduler)
  - VMware integration for hybrid environment:
    - pyvmomi library for vSphere API integration
    - vCenter Server API for managed ESXi host
    - Direct ESXi host API for standalone host
    - Support for both vCenter-managed and standalone ESXi hosts

**OS Decision Notes:**
Rocky Linux 9.6 is an excellent choice because:
- ✅ **LTS Support:** Rocky Linux 9.x has support until ~2032 (matches RHEL 9 lifecycle)
- ✅ **Stability:** Enterprise-grade, RHEL-compatible
- ✅ **Security:** Regular security updates and patches
- ✅ **Current:** Rocky 9.6 is recent (no urgent need to upgrade)
- ✅ **Package Ecosystem:** Excellent for web applications (Python, Node.js, databases)

**Recommendation:** Stay with Rocky Linux 9.6 - it's perfect for this project.

**Next Steps:**
1. Document all desired functions using the template above
2. Discuss and refine each function
3. Prioritize functions and organize into development phases
4. Create technical architecture based on requirements
5. Begin development planning
