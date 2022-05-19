In order to set up your computer for nightwatch testing, follow these steps:
    1) Install Node.js onto your local computer from here - https://nodejs.org/en/download/
       Make sure to install the correct version depending on your computer and follow the 
       installers steps.
    2) Verify that Node has successfully installed onto your computer by running the following 
        command: "node -v" (The correct version should appear in the terminal)
    3) Verify that npm has successfully installed by typeing the following command : "npm -v"
        (The version should appear on your terminal output)
    4) Install npm into your local branch/path by running "npm install". Wait untill the message has successfully
       indicated a correct install (Warning messages can be ignored)
    5) Verify that the install was successful by running the following command " npm run serve:dev"
       If successful, the front-end server should be running in the background and going to the website
       "http://localhost:8080/" should launch you to the SAFA website. (DO NOT TERMINATE THE NPM PROGRAM. This
       is essential to get tests to work)
    5) Install the nightwatch module by running the following command: "npm install nightwatch --save-dev"
       (Ingnore any warnings)
    6) Install chromedriver by running the following command: "npm install chromedriver --save-dev"
       (Ignore any warnings given by the terminal)
    7) Once the above steps have been installed, run "npm test" to see if nightwatch has installed correctly.
       If correctly installed, the test should run as normal.
       