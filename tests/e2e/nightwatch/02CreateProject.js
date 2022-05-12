/*************************************************************************************************************
CreateProject.js - Created by: Jeremy Arellano
    This test will create a project from the project creator and verify that it has succsessfully
    created a project. Throughout the test, Nightwatch will verify that no errors occur durring the process,
    and that the user has succsessfully reached the TIM graph page.

    Some Notes:
        - This is where I will put any errors or bugs that I encounter throughout the testing process.
***********************************************************************************************************/

module.exports = {
    '@disabled': false,
    '@tags' : ['SAFA'],
    'Create Project Test'(browser) {
        const page = browser.page.UI_Interaction();

        /* Our constants will go here */
        const urlLandingPage = "http://localhost:8080/login";
        const projectCreatorButtonName = 'Continue';
        const HazardsFileName = 'Hazard.csv';
        const TestDataLocation = 'tests/e2e/nightwatch/TestData/';
        const screenShotDestination = '/02CreateProject/';


        /* Our test will occur here */
        page
            .navigate()
            .waitForElementVisible('@loginImageIcon', 5000, "WebAPI: URL loaded successfully")
            .assert.titleEquals('SAFA', 'UI: Title is correct') // Note, succsess in running the program so far
            .loginSession(screenShotDestination, 'Login_Success.png')

            .fillInTextBox('SAFA', 'Project Name')
            .fillInTextBox('Safety Artifact Forest Analysis', 'Project description')
            .takeScreenShot(screenShotDestination + 'ProjectNameEntered.png')
            .clickButton(projectCreatorButtonName)  
            .takeScreenShot(screenShotDestination + 'ProjectFileUpload.png')

            /* Now lets test if we can succsesfully upload a file for Hazards */
            .clickButton(' Create new artifact')
            .fillInTextBox('Hazards', 'Artifact Name')
            .clickButton(' Create Artifact ')
            .takeScreenShot(screenShotDestination + 'ArtifactUploadScreen.png')
            .uploadFileWithParameters('@HazardsUploadButton', TestDataLocation, HazardsFileName)
            .pause(1000)

            .clickButton(' Create new artifact')
            .fillInTextBox('Requirements', 'Artifact Name')
            .clickButton(' Create Artifact ')
            .uploadFileWithParameters('@RequirementsUploadButton', TestDataLocation, 'Requirement.csv')
            .pause(1000)

            .clickButton(' Create new artifact')
            .fillInTextBox('Designs', 'Artifact Name')
            .clickButton(' Create Artifact ')
            .uploadFileWithParameters('@DesignsUploadButton', TestDataLocation, 'Design.csv')
            .pause(1000)
    
            .clickButton(' Create new artifact')
            .fillInTextBox('Environmental Assumptions', 'Artifact Name')
            .clickButton(' Create Artifact ')
            .uploadFileWithParameters('@EnvironmentalAssumptionsUploadButton', TestDataLocation, 'EnvironmentalAssumption.csv')
            .pause(1000)

            .clickButton(projectCreatorButtonName)
            .pause(500)
            .takeScreenShot(screenShotDestination + 'Artifacts_Successfully_Uploaded.png')

            /* Now lets upload the Trace Links */
            .clickButton(' Create new trace link')
            .clickButton(' Select Source ')
            .pause(100)
            .useXpath()
            .click(`//*[contains(text(),'Requirements') and @class="v-btn__content" ]`)
            .clickButton(' Select Target ')
            .useXpath()
            .click(`//*[contains(text(),'Hazards') and @class="v-btn__content"]`)
            .clickButton('Create Link')
            .uploadFileWithParameters('@Requirement2HazardsUploadButton', TestDataLocation, 'Requirement2Hazard.csv')
            .pause(100)
            .takeScreenShot(screenShotDestination + 'Error.png')
            
            
            .clickButton(' Create new trace link')
            .clickButton(' Select Source ')
            .pause(100)
            .useXpath()
            .click(`//*[contains(text(),'Environmental Assumptions') and @class="v-btn__content" ]`)
            .clickButton(' Select Target ')
            .useXpath()
            .click(`//*[contains(text(),'Hazards') and @class="v-btn__content"]`)
            .clickButton('Create Link')
            .uploadFileWithParameters('@Environmental2HazardsUploadButton', TestDataLocation, 'EnvironmentalAssumption2Hazard.csv')
            .pause(90000)
            
            /*
            .pause(100)
            .useXpath()
            .click(`//*[contains(text(),'Design')]`)
            .useCss()
            .clickButton(' Select Target ')
            .pause(100)
            .clickButton('Requirements')
            .clickButton('Create Link')
        */
    }
};