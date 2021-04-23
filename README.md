# Running SAFA Services API Locally

## Installation Requirements
Node.js v12+ https://nodejs.org/en/ \
Docker MacOS: https://docs.docker.com/docker-for-mac/ Or for Windows: https://docs.docker.com/docker-for-windows/ \
Docker Compose https://docs.docker.com/compose/install/

## Project Requirements
Jira Project Access for: http://spwd.cse.nd.edu:8080/ \
GitHub Read Access for: https://github.com/SAREC-Lab/Dronology

Log into Jira:
 1. Open a browser window, and navigate to http://spwd.cse.nd.edu:8080/
 1. Log in with your credentials and close browser

Double check to make sure that you have access to https://github.com/SAREC-Lab/Dronology/

## Changes to SAFA-services-api
```bash
$ cd SAFA-services-api/src/main/resources/
```

1. Open `application.properties`
1. Delete all the text in file
1. Paste text below into the file
1. Fill out jira.username, jira.password, git.username, git.password
 
```bash
src/main/resources/Application.properties:
/src/main/resources
neo4j.username=neo4j
neo4j.password=secret
neo4j.host=localhost
neo4j.port=7687
neo4j.scheme=bolt
jira.username=
jira.password=
git.url=https://github.com/SAREC-Lab/Dronology.git
git.branch=ICSE_2019_DATA_V1
git.username=
git.password=
```
## Build SAFA-services-api
```bash
cd SAFA-services-api
```

```bash
docker build . -t safa-api
```

## SAFA
```bash
cd SAFA
```

1. Open `application.properties`
1. Delete all the text in file
1. Paste text below into the file
1. Fill out jira.username, jira.password, git.username, git.password
 
```bash
docker-compose up
```

Both neo4j and SAFA Services API should be up and running now

## Changes to SAFA-Vue
```bash
cd SAFA-Vue/config/
```
1. Open `default.json`
1. Change `"url": "https://safa.crc.nd.edu"` to `"url": "http://localhost:8080"`

```bash
cd SAFA-Vue
```

```bash
npm run dev
```

## Electron

1. When Electron opens the database is originally empty.
1. In Electron click on Project->Synchronize Forest
1. This should update the database and the trees should appear.

## Update Application with Backend Changes
```bash
cd SAFA-services-api
```
```bash
docker build . -t safa-api
```
```bash
cd SAFA
```

```bash
docker-compose up
```
Backend change should appear on electron. If not click on Project->Synchronize Forest

## Neo4j Username and Password for Logging into Neo4j Browser Interface
Username: neo4j \
Password: secret \
Helpful command to delete all Neo4j data: (ONLY USE ON LOCAL NEO4J INSTANCE) \
```MATCH (n)
DETACH DELETE n
```

## MySQL Command Line Login:
```docker exec -it mysql-db mysql -uroot -p``` \
Password: secret2 \
```use safa-db```

## Backend Flatfile Workflow
https://docs.google.com/document/d/1z2j8eH8UfnCP5d9z2G-0B6a83mtnvlAS_0aclvhZBLs/edit?usp=sharing

## Known Problems Google Doc Link

https://docs.google.com/document/d/10BCZqpCamrEYQa5RNjLQl_gHcCQc7RFusLTfo2OH_mA/edit?usp=sharing
