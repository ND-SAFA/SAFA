/**********************************************************
FirstLoginTest.js - Created by: Jeremy Arellano
    This simple test will automate the login process and
    verify that it has succsessfully reached the create
    project screen or viceverse

    Some Notes:
        - This is where I would leave notes in case I get 
            stuck or reach a bug in testing
***********************************************************/

module.exports = {
    
    '@tags' : ['SAFA'],
    'Login Attempt'(browser) {
        /* Our constants will go here */
        const userNameFilledInBox = 'jarella2@nd.edu';
        const userNameFilledInBoxPassword = 'Cps44342847';
        const loginPageEmailResponseBox = 'input[type="text"]'; // This is an id and is labled with a #
        const loginPagePasswordResponseBox = 'input[type="password"]'
        const loginPageButtonResponse = 'button[type="button"][class="v-btn v-btn--is-elevated v-btn--has-bg theme--light v-size--default primary"]'

        /* Our test will occur here */
        browser
            .url('http://localhost:8080/') // Note, succsess in running the program so far
            .setValue(loginPageEmailResponseBox, userNameFilledInBox)
            .setValue(loginPagePasswordResponseBox,userNameFilledInBoxPassword)
            .saveScreenshot('tests_output/screenshots/login.png') // Information is succsessfully filled in
            .click(loginPageButtonResponse) // Now we want to log into the login page and progress
            .pause(3000) // Pause so that the screen can update
            .saveScreenshot('tests_output/screenshots/succsessLogin.png') // Succsess here


    }
};