# SAFA - Safety Artifact Forest Analysis

## Overview

SAFA (Safety Artifact Forest Analysis) is a comprehensive multi-component system designed for analyzing safety artifacts and trace links. The platform consists of three integrated applications: a Spring Boot backend API (bend) built with Java 17 and Gradle, a Vue 3 frontend application (fend) using TypeScript and Quasar framework, and a Django-based generation API (gen-api) with Python and Celery for AI-powered analysis and document generation. The system leverages advanced language models through the tgen component and shared utilities via gen-common to provide intelligent safety artifact analysis and traceability management.

## Getting Started

### Prerequisites

Before running the application, you need to create a `.env` file in the root directory with your API keys and credentials:

- OPEN_AI_KEY and OPEN_AI_ORG: OpenAI API credentials
- ANTHROPIC_API_KEY: Anthropic API key for LLM operations
- AWS credentials: BACKEND_ACCESS_ID, BACKEND_SECRET_KEY, BACKEND_BUCKET_NAME, SAGEMAKER_ROLE

### Running the Application

To run the entire SAFA stack locally:

```bash
docker compose up --build -d
```
or
```bash
./start.sh
```

This will start all services:
- **fend** (Frontend): Available at http://localhost:8080
- **bend** (Backend API): Available at http://localhost:3000
- **gen** (Generation API): Available at http://localhost:4000
- **mysql** (Database): Available at localhost:3306
- **redis** (Message Broker): Used for task queue management
