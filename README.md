# Installation

1. Install package libraries : `npm install`
2. Choose a backend environment: local, development, production
   1. Local
      1. Make sure you have an instance of the backend running at http://localhost:8080
      2. `npm run serve:local`
   2. Development and Production
      1. Download .env files from notion and place at the top of the project folder
      2. `npm run serve:dev` to target deployed development branch
      3. `npm run serve:prod` to target deployed production branch
