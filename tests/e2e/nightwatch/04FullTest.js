/*********************************************************
FullTest.js - Created by: Jeremy Arellano
    This automated test will test the capabilities of the SAFA
    web application in terms of creating a new account, logging in,
    creating a project, manipulating the graph, and logging out. 
    This test will also verify components of the UI are working properly 
    and that no errors occur during the process. 

    Some Notes:
        - Previous Tests (such as 01-03) will be used to test the functionality of individual parts of the
            web application. However, components of these tests will be seen in this test file.
        - Currently, there is no way to delete an account, therefore the Create account section of the test 
            will be skipped as to avoid creating too many spam accounts. In the later future, this section can
            be commented back into the test.
*********************************************************/

module.exports = {
    '@disabled': false,
    '@tags' : ['SAFA'],
    'SAFA Website Demo Test'(browser) {
        /* Page object file */
        const page = browser.page.UI_Interaction();

        /* Screenshot Destination */
        const screenShotDestination             = '/04FullTest/';

        /* Test Data Location + Names */
        const TestDataLocation                  = 'tests/e2e/nightwatch/TestData/';
        const HazardsFileName                   = 'Hazard.csv';
        const RequirementsFileName              = 'Requirement.csv';
        const DesignsFileName                   = 'Design.csv';
        const EnvironmentalAssumptionsFileName  = 'EnvironmentalAssumption.csv';

        /* Login Information */
        const userName                          = 'nightwatch1@test.com';
        const password                          = 'nightwatch123!';

        /* Element Text Values */
        const accountCreationSuccessfulTitle    = 'Welcome to SAFA!';
        const projectCreatorContinueButton      = 'Continue';
        const projectCreatorName                = 'Project Name';
        const projectCreatorDescription         = 'Project description';
        const newArtifactButton                 = 'Create new artifact';
        const createArtifactButton              = 'Create Artifact';
        const createNewArtifactButton           = 'Create new artifact';
        const artifactNameInputField            = 'Artifact Name';
        const deleteArtifactButton              = 'Delete';



        page 
            /* Navigate to the website and verify elements have properly loaded */
            .logToConsole('Navigating to the website')
            .navigate()
            .waitForElementVisible('@loginImageIcon', 5000, "WebAPI: URL loaded successfully")
            .assert.titleEquals('SAFA', 'UI: Title is correct')
            .buttonNotClickable('Login', 'UI: Login button is disabled')
            .takeScreenShot(screenShotDestination + 'Login_Success.png')

            /* Create a new account */
            .logToConsole('Creating a new account')
            .logToConsole('    Skipping account creation for now')
            //.clickButton('Sign Up')
            //.fillInTextBox(userName, 'Email')
            //.buttonNotClickable('Create Account', 'UI: Create Account button is disabled without entering a password')
            //.fillInTextBox(password, 'Password')
            //.takeScreenShot(screenShotDestination + 'CreateAccount.png')
            //.clickButton('Create Account')
            //.checkText(accountCreationSuccessfulTitle, "UI: Account Creation Successful")
            //.clickButton('Login')

            /* Login to the website */
            .logToConsole('Logging into the website')
            .loginSession(screenShotDestination, 'Login_Success.png', userName, password, true)
            .waitForElementNotPresent('@emailInputField', 5000, "WebAPI: Email and Passwod fields are not visible")
            .waitForElementVisible('@projectCreationSteps', 5000, "UI: Project creator is visible")
            .assert.visible('@webTitleGlobal', 'UI: Web title is visible')

            /* Naming a New Project */
            .logToConsole('Naming a new project')
            .buttonNotClickable(projectCreatorContinueButton, 'UI: Cannot continue in project creator without naming our project')
            .fillInTextBox('Test Project', projectCreatorName)
            .buttonClickable(projectCreatorContinueButton, 'UI: Continue button is enabled after naming our project without a description')
            .fillInTextBox('This is a test project', projectCreatorDescription)
            .clickButton(projectCreatorContinueButton)
            .takeScreenShot(screenShotDestination + 'Nameing_successful.png')

            /* Uploading Artifact */
            .logToConsole('Uploading an artifact')
            .assert.visible('@artifactCreatorWarning', 'UI: Artifact creator warning is visible')
            .buttonNotClickable(projectCreatorContinueButton, 'UI: Cannot continue in project creator without creating at least one artifact')
            .clickButton(newArtifactButton)
            .takeScreenShot(screenShotDestination + 'Artifact_Name_Given.png')
            .buttonNotClickable(createNewArtifactButton, 'UI: Cannot create an artifact without any information given')
            .clickButton(createArtifactButton)
            .assert.visible('@artifactCreatorWarning', 'UI: Artifact creator warning is visible when no name is given')
            .takeScreenShot(screenShotDestination + 'Artifact_No_Name_Given.png')
            .fillInTextBox(HazardsFileName, artifactNameInputField)
            .clickButton(createArtifactButton)
            .uploadFileWithParameters(TestDataLocation, HazardsFileName)
            .assert.visible('@checkMarkIcon', "UI: Hazards file upload was successful and without errors")
            .buttonClickable(projectCreatorContinueButton, 'UI: Continue button is enabled after uploading one artifact')
            .takeScreenShot(screenShotDestination + 'Artifact_Upload_Successful.png')


            /* Deleting an Artifact */
            .logToConsole('Deleting an artifact')
            .click('@dropDownIcon')
            .clickButton(deleteArtifactButton)
            .assert.not.elementPresent('@checkMarkIcon', "UI: Artifact was successfully deleted from the project creator")


            /* Creating the rest of the artifacts for this test */
            .logToConsole('Uploading the remaining artifacts')
            .clickButton(newArtifactButton)
            .fillInTextBox(RequirementsFileName, artifactNameInputField)
            .clickButton(createArtifactButton)
            .uploadFileWithParameters(TestDataLocation, RequirementsFileName)
            .assert.visible('@checkMarkIcon', "UI: Requirements file upload was successful and without errors")

            .clickButton(newArtifactButton)
            .fillInTextBox(DesignsFileName, artifactNameInputField)
            .clickButton(createArtifactButton)
            .uploadFileWithParameters(TestDataLocation, DesignsFileName)
            .assert.visible('@checkMarkIcon', "UI: Designs file upload was successful and without errors")

            .clickButton(newArtifactButton)
            .fillInTextBox(EnvironmentalAssumptionsFileName, artifactNameInputField)
            .clickButton(createArtifactButton)
            .uploadFileWithParameters(TestDataLocation, EnvironmentalAssumptionsFileName)
            .assert.visible('@checkMarkIcon', "UI: Environmental Assumptions file upload was successful and without errors")

            .clickButton(newArtifactButton)
            .fillInTextBox(HazardsFileName, artifactNameInputField)
            .clickButton(createArtifactButton)
            .uploadFileWithParameters(TestDataLocation, HazardsFileName)
            .assert.visible('@checkMarkIcon', "UI: Hazards file upload was successful and without errors")

            .takeScreenShot(screenShotDestination + 'Artifact_Creation_Successful.png')
            .clickButton(projectCreatorContinueButton)

            /* Upload Trace Links */
            .logToConsole('Uploading Trace Link')
            .assert.visible('@traceLinkCreatorWarning', 'UI: Trace Link creator warning is visible')
            .buttonNotClickable(projectCreatorContinueButton, 'UI: Cannot continue in project creator without creating at least one trace link')
            .clickButton()

            
            /* Logout of the website */
            .logToConsole('Logging out of the website')
            .click('@ProfilePictureAttributes')
            .clickButton('Logout')
            .waitForElementVisible('@loginImageIcon', 5000, "WebAPI: User successfully logged out")
            .takeScreenShot(screenShotDestination + 'Logout_Success.png')

            /* End of test */
            .end();
        


    }
};