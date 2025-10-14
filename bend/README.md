# Build Status

| Branch | Status                                                                                                                                                          |
|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dev    | [![dev](https://github.com/ND-SAFA/bend/actions/workflows/safa.yaml/badge.svg?branch=development)](https://github.com/ND-SAFA/bend/actions/workflows/safa.yaml) |
| prod   | [![prod](https://github.com/ND-SAFA/bend/actions/workflows/safa.yaml/badge.svg?branch=production)](https://github.com/ND-SAFA/bend/actions/workflows/safa.yaml) |

# Running SAFA Services API Locally

## Installation Requirements

Node.js v12+ https://nodejs.org/en/ \
Docker MacOS: https://docs.docker.com/docker-for-mac/ Or for Windows: https://docs.docker.com/docker-for-windows/ \
Docker Compose https://docs.docker.com/compose/install/

## Getting Started

To get the stack running on your localhost port 8080 then run:
`docker-compose up`:

In order to delete any docker data associated with the database of the api run:

`docker-compose down -v`

# TODO

## Broken Features

1. Turn off account verification
2. Turn off transaction service and balance checking

## Tech Debt

1. Centralize the conversion between [Name]Version to [Name]AppEntity.
2. Flat files should automatically check if properties passed in can be fullfilled.
