/*************************************************************************************************************
CreateProject.js - Created by: Jeremy Arellano
    This test will create a project from the project creator and verify that it has succsessfully
    created a project. Throughout the test, Nightwatch will verify that no errors occur durring the process,
    and that the user has succsessfully reached the TIM graph page.

    Some Notes:
        - This is where I will put any errors or bugs that I encounter throughout the testing process.
***********************************************************************************************************/

module.exports = {
    '@tags' : ['SAFA'],
    'Create Project Test'(browser) {
        /* Our constants will go here */
        const urlLandingPage = "http://localhost:8080/login";
        const projectCreatorButtonName = 'Continue';
        const HazardsFileName = 'Hazards.csv';

        /* Our test will occur here */
        browser
            .url(urlLandingPage) // Note, succsess in running the program so far
            .waitForElementVisible('body', "WebAPI: URL loaded successfully")
            .assert.titleEquals('SAFA', 'UI: Title is correct') // Note, succsess in running the program so far
        
        loginSession(browser);
        fillInTextBox('Project Name', 'SAFA', browser);
        fillInTextBox('Project description', 'Saftey Artifact Forest Analysis', browser);
        takeScreenShot('ProjectNameEntered.png')
        //browser
            //.useXpath()
            //.getAttribute(`//*[contains(text(),'${projectCreatorButtonName}')][not(@disabled)]`, 'disabled', function(result) {this.assert.equal(result.value, null, "Button is Disabled");}) // This currently does not work
            //.useCss()
        clickButton(projectCreatorButtonName, browser);
        browser.waitForElementVisible('body')
        takeScreenShot('ProjectFileUpload.png')

        /* Now lets test if we can succsesfully upload a file */
        clickButton(' Create new artifact', browser);
        fillInTextBox('Artifact Name', 'Hazards', browser);
        clickButton(' Create Artifact ', browser);
        takeScreenShot('ArtifactUploadScreen.png')
        uploadFile('File', HazardsFileName, browser);
        takeScreenShot('ArtifactUploaded.png')


    },

        

};

function clickButton(lableName, browser) {
    browser.useXpath();
    browser.assert.visible(`//*[contains(text(),'${lableName}')]`, function(results){
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

function takeScreenShot(fileName) {
    browser.saveScreenshot(`tests/e2e/nightwatch/screenshots/CreateProject/${fileName}`);
}

function loginSession(browser) {
    /* Our constants will go here */
    const userNameFilledInBox = 'jarella2@nd.edu'
    const userNameFilledInBoxPassword = 'Cps44342847'
    const loginButtonName = ' Login ';

    fillInTextBox('Email', userNameFilledInBox, browser)
    fillInTextBox('Password', userNameFilledInBoxPassword, browser)
    takeScreenShot('CredetialsEntered.png');
    clickButton(loginButtonName, browser)
    browser.waitForElementVisible('body')
}

function uploadFile(textBoxName,fileName ,browser) {
    /* This function will upload a file to the project */
    browser
        .click(`button[type="button"][aria-label="prepend icon"]`)
        .execute(`document.querySelectorAll('input[type=file]')[0].style.display = 'block'`)
        .pause(1000)
        .useXpath()
        .waitForElementVisible(`//*[contains(text(),'${textBoxName}')]`) ////*[contains(text(),'File')]/following-sibling::input[@type="file"]
        //.waitForElementVisible(`//*[contains(text(),'${textBoxName}')]/following-sibling::input[@type="file"]`)
        .useCss()
        .setValue(`input[type=file]`, require('path').resolve(__dirname +'../TestData/' + fileName))
        .pause(1000)


    
    /*
    results => {
        if (results.value) {
            const textBoxLocation = `//*[contains(text(),'File')]/following-sibling::input[@type="file"]`;
            browser.click(`//*[contains(text(),'File')]/`).setValue( textBoxLocation, require('path').resolve(__dirname + '../TestData/' + fileName));
            browser.useCss();
            return "UI: {textBoxName} Uploaded succsessfully";
        } else {
            browser.useCss();
            return "UI: {textBoxName} failed to upload";
        } 
    
    });
    */
}