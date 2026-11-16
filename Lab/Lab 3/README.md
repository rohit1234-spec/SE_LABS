# Lab 3: Architectural Design & Component Modeling

**Student:** C Rohit Reddy  
**SRN:** PES2UG24CS125  
**Course:** Software Engineering (SETA Labs)  
**Problem Statement:** Smart Lab Equipment & Slot Reservation Portal  

---

## Overview

Lab 3 focuses on high-level software architecture and component decomposition for the **Smart Lab Equipment & Slot Reservation Portal**.

### Architecture Selected: Layered Architecture (4-Tier)
The system is decomposed into four discrete, loosely coupled layers:
1. **Presentation Layer:**
   - Web Portal UI & Mobile Client interfaces for Students and Lab Technicians.
   - Provides catalog views, real-time availability calendars, and technician dashboard widgets.
2. **Business / Application Logic Layer:**
   - Reservation Controller: Manages reservation workflows, validations, and cancellation rules.
   - Slot & Equipment Availability Manager: Performs real-time conflict checking and lock acquisition.
   - Technician Inventory Manager: Governs equipment maintenance status and capacity limits.
   - Notification Service: Dispatches booking receipts and reminders.
3. **Data Access Layer (DAL):**
   - Object-Relational Mapping (ORM) and data abstraction repositories.
   - Enforces transactional ACID boundaries and row-level locking to prevent double bookings.
4. **Database & Storage Layer:**
   - Relational Database (PostgreSQL / MySQL) maintaining student accounts, equipment catalogs, slot schedules, and reservation ledgers.

### Documents Included:
1. **Component Diagram (`SE_Lab3_Component_Diagram.pdf`)**:
   - Visualizes structural decomposition into modular components, provided interfaces (`<<interface>>`), and required dependencies.
2. **Architecture Justification Report (`SE_Lab3_Architecture_Justification.pdf`)**:
   - Formal technical justification detailing why Layered Architecture was selected, trade-off analysis versus microservices, separation of concerns, and maintainability.
