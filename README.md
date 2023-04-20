[![dev](https://github.com/ND-SAFA/bend/actions/workflows/safa.yaml/badge.svg?branch=development)](https://github.com/ND-SAFA/bend/actions/workflows/safa.yaml)
[![prod](https://github.com/ND-SAFA/bend/actions/workflows/safa.yaml/badge.svg?branch=production)](https://github.com/ND-SAFA/bend/actions/workflows/safa.yaml)

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
