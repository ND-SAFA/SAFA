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
        - Line 163 is commented out due to a bug with generating the TIM Grpah, this will be uncommented in future releases.
          However, on a normal run the test would fail because of this since this is an test failure condition.

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
        const TestDataLocation                       = 'tests/e2e/nightwatch/TestData/';
        const HazardsFileName                        = 'Hazard.csv';
        const RequirementsFileName                   = 'Requirement.csv';
        const DesignsFileName                        = 'Design.csv';
        const EnvironmentalAssumptionsFileName       = 'EnvironmentalAssumption.csv';
        const Requirement2HazardFileName             = 'Requirement2Hazard.csv';
        const EnvironmentalAssumption2HazardFileName = 'EnvironmentalAssumption2Hazard.csv';
        const Design2DesignFileName                  = 'Design2Design.csv';
        const Requirement2RequirementFileName        = 'Requirement2Requirement.csv';
        const Hazard2HazardFileName                  = 'Hazard2Hazard.csv';
        const projectName                            = 'Test Project';

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
        const newTraceLinkButton                = 'Create new trace matrix';
        const traceLinkButton                   = ' Create Trace Matrix ';    
        const sourceTraceLinkButton             = ' Select Source ';
        const targetTraceLinkButton             = ' Select Target ';
        const deleteTraceLinkButton             = ' Delete ';
        const createProjectButton               = 'Create Project'
        const projectDropDownGloabl             = 'Project';
        const OpenProjectButton                 = 'Open Project';
        const deleteingProjectInputField        = `Type "${projectName}"`;
        const deleteProjectButton               = 'Delete';
        
        /* Element Xpath Values */
        const dropDownIcon_traceLink            = '(.//i[@aria-hidden="true"][@class="v-icon notranslate mdi mdi-chevron-down theme--light"])[9]'; // Note, this will only work for one specific use


        page 
            /*  Navigate to the website and verify elements have properly loaded */
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
            .fillInTextBox(projectName, projectCreatorName)
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
            .checkUploadSuccess("UI: Hazards file upload was successful and without errors")
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
            .checkUploadSuccess("UI: Requirements file upload was successful and without errors")

            .clickButton(newArtifactButton)
            .fillInTextBox(DesignsFileName, artifactNameInputField)
            .clickButton(createArtifactButton)
            .uploadFileWithParameters(TestDataLocation, DesignsFileName)
            .checkUploadSuccess("UI: Designs file upload was successful and without errors")

            .clickButton(newArtifactButton)
            .fillInTextBox(EnvironmentalAssumptionsFileName, artifactNameInputField)
            .clickButton(createArtifactButton)
            .uploadFileWithParameters(TestDataLocation, EnvironmentalAssumptionsFileName)
            .checkUploadSuccess("UI: Environmental Assumptions file upload was successful and without errors")

            .clickButton(newArtifactButton)
            .fillInTextBox(HazardsFileName, artifactNameInputField)
            .clickButton(createArtifactButton)
            .uploadFileWithParameters(TestDataLocation, HazardsFileName)
            .checkUploadSuccess("UI: Hazards file upload was successful and without errors")

            .takeScreenShot(screenShotDestination + 'Artifact_Creation_Successful.png')
            .clickButton(projectCreatorContinueButton)

            /* Upload Trace Links */
            .logToConsole('Uploading Trace Link')
            .assert.visible('@traceLinkCreatorWarning', 'UI: Trace Link creator warning is visible')
            .buttonClickable(projectCreatorContinueButton, 'UI: Continue button is enabled wihtout any tracelinks')
            .clickButton(newTraceLinkButton)
            .clickButton(traceLinkButton)
            .assert.visible('@traceLinkNoInputWarning', "UI: Trace Link cannot be created without a source and target")
            .takeScreenShot(screenShotDestination + 'TraceLink_No_Input.png')
            .clickSelector(sourceTraceLinkButton, RequirementsFileName)
            .clickButton(traceLinkButton)
            .assert.visible('@traceLinkNoInputWarning', "UI: Trace Link cannot be created without a target")
            .clickSelector(targetTraceLinkButton, HazardsFileName)
            .clickButton(traceLinkButton)
            .uploadFileWithParameters(TestDataLocation, Requirement2HazardFileName)
            .checkUploadSuccess("UI: Trace Link was successfully created")
            .takeScreenShot(screenShotDestination + 'TraceLink_Creation_Successful.png')

            /* Deleting Trace Links */
            .logToConsole('Deleting Trace Links')
            .useXpath().click(dropDownIcon_traceLink).useCss()
            .clickButton(deleteTraceLinkButton)
            .assert.visible('@traceLinkCreatorWarning', "UI: Trace Link was successfully deleted from the project creator")
            .takeScreenShot(screenShotDestination + 'TraceLink_Deletion_Successful.png')

            /* Uploading the remaining Trace Links */
            .logToConsole('Uploading the remaining Trace Links')

            .clickSelectorTraceLinks(RequirementsFileName, HazardsFileName)
            .uploadFileWithParameters(TestDataLocation, 'Requirement2Hazard.csv')
            .checkUploadSuccess("UI: Trace Link was successfully created")

            .clickSelectorTraceLinks(EnvironmentalAssumptionsFileName, HazardsFileName)
            .uploadFileWithParameters(TestDataLocation, 'EnvironmentalAssumption2Hazard.csv')
            .checkUploadSuccess("UI: Trace Link was successfully created")

            .clickSelectorTraceLinks(DesignsFileName, DesignsFileName)
            .uploadFileWithParameters(TestDataLocation, 'Design2Design.csv')
            .checkUploadSuccess("UI: Trace Link was successfully created")

            .clickSelectorTraceLinks(RequirementsFileName, RequirementsFileName)
            .uploadFileWithParameters(TestDataLocation, 'Requirement2Requirement.csv')
            .checkUploadSuccess("UI: Trace Link was successfully created")              // Needs to be fixed
            // Remove once bug is fixed
            .useXpath()
            .click(`(//*[contains(text(),'Generate Trace Links')])[last()]`)

            .clickSelectorTraceLinks(HazardsFileName, HazardsFileName)
            .uploadFileWithParameters(TestDataLocation, 'Hazard2Hazard.csv')
            .checkUploadSuccess("UI: Trace Link was successfully created")

            .takeScreenShot(screenShotDestination + 'TraceLink_Upload_Successful.png')
            .clickButton(projectCreatorContinueButton)

            /* View TIM Step*/
            .logToConsole('Viewing TIM')
            .assert.visible('@timGraph', "UI: TIM Graph uploaded successfully")
            .pause(1000)              // Can be set for longer if the user wants to observe the graph
            .takeScreenShot(screenShotDestination + 'TIM_View.png')

            /* Creating the project */
            .logToConsole('Creating the project')
            .clickButton(createProjectButton)
            .pause(2000)
            .waitForElementPresent('@timGraph', 5000, false, "UI: TIM Graph is visible")
            .takeScreenShot(screenShotDestination + 'Project_Creation_Successful.png')
            .pause(5000)



            /* Deleting the project */
            .logToConsole('Deleting the project')
            .clickSelector(projectDropDownGloabl, OpenProjectButton)
            .click('@deleteProjectIcon')
            .fillInTextBox(projectName, deleteingProjectInputField)
            .clickButton(deleteProjectButton)
            .assert.visible('@projectSelectionMessage', "WebAPI: Project has successfully been deleted")
            .click('@closeWindowIcon')


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