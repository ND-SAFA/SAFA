# SAFA - Safety Artifact Forest Analysis

## Overview

SAFA (Safety Artifact Forest Analysis) is a comprehensive multi-component system designed for analyzing safety artifacts and trace links. The platform consists of three integrated applications: a Spring Boot backend API (bend) built with Java 17 and Gradle, a Vue 3 frontend application (fend) using TypeScript and Quasar framework, and a Django-based generation API (gen-api) with Python and Celery for AI-powered analysis and document generation. The system leverages advanced language models through the tgen component and shared utilities via gen-common to provide intelligent safety artifact analysis and traceability management.

## Getting Started

### Prerequisites

Before running the application, you need to create a `.env` file in the root directory with your configuration:

**Required:**
- `OPEN_AI_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key for LLM operations
- `MYSQL_ROOT_PASSWORD`: MySQL root password
- `MYSQL_USER`: MySQL user
- `MYSQL_PASSWORD`: MySQL password
- `MYSQL_DATABASE`: Database name (defaults to `safa-db`)

**Optional - Demo Project Configuration:**
- `DEMO_EMAIL`: Email for demo account (enables `/demo` route)
- `DEMO_PASSWORD`: Password for demo account
- `DEMO_PROJECT_VERSION`: Project version ID to show in demo

**Optional - AWS credentials (if using AWS features):**
- `BACKEND_ACCESS_ID`, `BACKEND_SECRET_KEY`, `BACKEND_BUCKET_NAME`, `SAGEMAKER_ROLE`

Example `.env` file:
```bash
# API Keys
OPEN_AI_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# MySQL Configuration
MYSQL_ROOT_PASSWORD=secret2
MYSQL_USER=user
MYSQL_PASSWORD=secret3
MYSQL_DATABASE=safa-db

# Demo Account (Optional)
DEMO_EMAIL=demo@example.com
DEMO_PASSWORD=demo123
DEMO_PROJECT_VERSION=your-project-version-id
```

### Running the Application

To run the entire SAFA stack:

```bash
docker compose up --build -d
```
or
```bash
./start.sh
```

This will start all services:
- **proxy** (Nginx): Routes traffic at http://localhost
- **fend** (Frontend): Accessible via proxy at http://localhost
- **bend** (Backend API): Accessible via proxy at http://localhost/api
- **gen** (Generation API): Internal service for AI operations
- **mysql** (Database): Internal service (no public exposure)
- **redis** (Message Broker): Internal service for task queue management

### User Management

Use the provided script to manage users:

```bash
./manage-users.sh
```

Features:
1. View all users
2. View user statistics
3. Verify user and promote to superuser
4. Verify user only
5. Promote user to superuser
6. Demote user from superuser
7. Delete user

### Demo Project

If you configured demo account credentials in `.env`, users can access a demo project at:
```
http://localhost/demo
```

The demo route auto-logs in with the demo account and navigates to the configured project.
