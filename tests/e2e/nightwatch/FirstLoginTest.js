/**********************************************************
FirstLoginTest.js - Created by: Jeremy Arellano
    This simple test will automate the login process and
    verify that it has succsessfully reached the create
    project screen. After the test is complete, the test will then logout and
    test if the logout process has succsessfully reached the login screen.

    Some Notes:
        - Currently, I am struggling to place my function calls into another
            file.  I am not sure how to do this, so for now I will just place
            them here.
        - Another Bug, I am not sure why but our tests for the button and input fields will
            spit out the text field name instead of the text field value.  I am not sure why it is doing 
            this but I will try to fix it.
***********************************************************/

module.exports = {
    '@tags' : ['SAFA'],
    'Login and Logoff Attempt'(browser) {
        /* Our constants will go here */
        const urlLandingPage = "http://localhost:8080/login";
        const userNameFilledInBox = 'jarella2@nd.edu';
        const userNameFilledInBoxPassword = 'Cps44342847';
        const checkProjectNumberSteps = '.v-stepper__header'
        const checkContinueButtonDisabled = '.container [type="button"].v-btn--outlined'
        const ProfilePictureAttributes = 'button[type="button"][role="button"]'
        
        /* Our test will occur here */
        browser
            .url(urlLandingPage) // Note, succsess in running the program so far
            .waitForElementVisible('body', 1000)
            .assert.titleEquals('SAFA', 'UI: Title is correct') // Note, succsess in running the program so far
   
        /* These functions will fill in the nessesary information to complete the login process */
        fillInTextBox('Email', userNameFilledInBox, browser)
        fillInTextBox('Password', userNameFilledInBoxPassword, browser)
        takeScreenShot("login.png");    // Take a screenshot of the login page
        clickButton(' Login ', browser) // This will click the login button if it exists
        browser.waitForElementVisible('body', 1000)
        takeScreenShot('LoginSuccess') // Succsess here

        browser
            /* Now lets test some elements on the page */
            .assert.urlContains('http://localhost:8080/create', 'Params: URL has changed to display the project creator')
            .assert.visible(checkProjectNumberSteps, 'UI: Project Step Counter Field is visible')
            .assert.attributeEquals(checkContinueButtonDisabled, 'enabled', null, 'UI: Button is disabled')
            .assert.visible(ProfilePictureAttributes, 'UI: Profile Picture is visible')

            /* Now lets Logout */  
            .click(ProfilePictureAttributes)
        takeScreenShot("Logout_Visibility.png");
        clickButton('Logout', browser)
        browser.useXpath().waitForElementVisible('//*[contains(text(), "Login")]', 1000, 'UI: Login Button is visible').useCss()
        takeScreenShot("logout.png");
    },
};

function clickButton(lableName, browser) {
    browser.useXpath();
    browser.assert.visible(`//*[contains(text(),'${lableName}')]`, results => {
        if (results.value) {
            //console.log("Button is visible");
            browser.click(`//*[contains(text(),'${lableName}')]`);
            browser.useCss();
            return "UI: Login Button is visible";
        } else {
            browser.useCss();
            return "UI: Login Button is not visible";
        } 
        
    }); 
}

function fillInTextBox(textBoxName, textBoxValue, browser) {
    browser.useXpath();
    browser.assert.visible(`//*[contains(text(),'${textBoxName}')]`, results => {
        if (results.value) {
            const textBoxLocation = `//*[contains(text(),'${textBoxName}')]/following-sibling::input`;
            browser.setValue( textBoxLocation, textBoxValue);
            browser.useCss();
            return "UI: {textBoxName} is visible";
        } else {
            browser.useCss();
            return "UI: {textBoxName} is not visible";
        } 
        
    }); 
}

function takeScreenShot(screenShotName) {
    /* This function will take a screenshot and save it to the correct location */
    browser.saveScreenshot(`tests/e2e/nightwatch/screenshots/${screenShotName}.png`);
}