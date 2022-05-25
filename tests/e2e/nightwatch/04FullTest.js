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
        - Some of the elements on the website currently could be renamed to have more distinction accrose from each other, this
           will make some elements separated from each other and easier to test.

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
        const F4NodeName                        = 'F4';
        const addArtifactButton                 = 'Add Artifact';
        const addArtifactInputField             = 'Artifact Name';
        const addArtifactTypeField              = 'Artifact Type';
        const addArtifactSummaryField           = 'Artifact Summary';
        const addArtifactBodyField              = 'Artifact Body';
        const testNodeName                      = 'Test_Node';
        const testNodeDescription               = 'This is a new node';
        const addArtifactSaveButton             = 'Save';
        
        
        /* Element Xpath Values */
        const dropDownIcon_traceLink            = '(.//i[@aria-hidden="true"][@class="v-icon notranslate mdi mdi-chevron-down theme--light"])[9]'; // Note, this will only work for one specific use
        const centerGraphButton                 = `span[class="v-btn__content"] i[aria-hidden="true"][class="v-icon notranslate mdi mdi-graphql theme--light"]`;
        const addArtifactHazardsOptionDropDown  = `(//div[contains(text(),'Hazard.csv') ])[last()]`
        let TIMNodelocation                     = {};
        const artifactTypeDropDown              = `(//label[contains(text(), 'Artifact Type')]/following-sibling::input)[1]`;
        const deleteProjectIcon                 = `button[class="v-btn v-btn--icon v-btn--round theme--light v-size--default"] span[class="v-btn__content"] i[aria-hidden="true"][class="v-icon notranslate mdi mdi-delete theme--light"]`
        const deleteProjectdeleteButton         = `button[type="button"][class="ml-auto v-btn v-btn--is-elevated v-btn--has-bg theme--light v-size--default error"] span[class="v-btn__content"]`;
        const openProjectCloseWindowButton      = `(.//button[@type="button"][@class="v-btn v-btn--icon v-btn--round theme--light v-size--default"]//span[@class="v-btn__content"]//i[@aria-hidden="true"][@class="v-icon notranslate mdi mdi-close theme--light"])[2]`;
        const artifactViewerTitle               = `.//h1[contains(text(), '${testNodeName}')]`;
        const artifactViewerDescription         = `.//p[contains(text(), '${testNodeDescription}')]`;  
        const newNodeArtifactTypeHazardOption   = '(//span[contains(text(), "Hazard")])[last()]';
        
        
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
            .pause(5000)
            .waitForElementPresent('@projectCreationSuccessfulMessage', 5000, true, "UI: Project success message appears in view")
            .takeScreenShot(screenShotDestination + 'Project_Creation_Successful.png')
            
            /* Testing TIM Graph Node */
            .logToConsole('Testing TIM Graph Node')
            .click(centerGraphButton)
            .findAndTestTIMNode(F4NodeName, TIMNodelocation, 0, 'UI: F4 Node was found and interactable')
            .useXpath().rightClick(TIMNodelocation.F4).useCss()
            .waitForElementVisible('@rightClickMenu', 5000, true, "UI: Right click menu is visible")
            .takeScreenShot(screenShotDestination + 'TIM_Node_Right_Click_Menu.png')

            /* Adding a new node to the graph */
            .logToConsole('Adding a new node to the graph')
            .click('@addArtifactButton')
            .fillInTextBox(testNodeName, addArtifactInputField)
            .fillInTextBox('Hazard.csv', addArtifactTypeField)
            .useXpath().click(newNodeArtifactTypeHazardOption).useCss()
            .fillInTextBox(testNodeDescription, addArtifactSummaryField)
            .fillInTextBox(testNodeDescription, addArtifactBodyField)
            .clickButton(addArtifactSaveButton)
            .click(centerGraphButton)
            .pause(1000)
            //.useXpath().waitForElementVisible(`//*[contains(text(),'${testNodeName}')]`, 5000, true, "UI: New node was added to the graph").useCss()            //.perform(() => { debugger; }) // This will hault execution in the chrome debugger
             
            .findAndTestTIMNode(testNodeName, TIMNodelocation, 0, 'UI: Test_Node was found and interactable')

            //.perform(() => { debugger; }) // This will hault execution in the chrome debugger))
            /* View Details of an Artifact */
            .logToConsole('Viewing Details of an Artifact')
            .useXpath().rightClick(TIMNodelocation.Test_Node).useCss()
            .moveToElement('@viewArtifactButton', undefined, undefined)
            .click('@viewArtifactButton')

            //.perform(() => { debugger; }) // This will hault execution in the chrome debugger

            .useXpath().waitForElementVisible(artifactViewerTitle, 5000, false, "UI: Artifact Viewer is Visible")
            .waitForElementVisible(artifactViewerDescription, 5000, false, "UI: Artifact Description is Visible").useCss()
            .takeScreenShot(screenShotDestination + 'ArtifactViewer.png')

            //.perform(() => { debugger; }) // This will hault execution in the chrome debugger
            
            /* Drag and Drop an Artifact */
            .logToConsole('Drag and Drop an Artifact')
            .click(centerGraphButton)
            .useXpath().moveToElement(`//*[contains(text(), '${testNodeName}')]`, undefined, undefined)
            .dragAndDrop(`//*[contains(text(), '${testNodeName}')]`, {x: 100, y: 100}).useCss()
            .takeScreenShot(screenShotDestination + 'Test_Node_Dragged.png')

            .perform(() => { debugger; }) // This will hault execution in the chrome debugger

            /* Adding a Link to an Artifact */
            .logToConsole('Adding a Link to an Artifact')
            .click(centerGraphButton)

            .perform(() => { debugger; }) // This will hault execution in the chrome debugger

            .useXpath().rightClick(TIMNodelocation.Test_Node).useCss()

            .perform(() => { debugger; }) // This will hault execution in the chrome debugger
            
            .moveToElement('@addLinkButton', undefined, undefined)
            .click('@addLinkButton')
            .useXpath().dragAndDrop(`//*[contains(text(), '${testNodeName}')]`, TIMNodelocation.F4).useCss()
            //.assert.visible('@linktoNodeIcon', "UI: Link was Successfully made") // cannot currently find the name of the arrow icon
            .takeScreenShot(screenShotDestination + 'Link_Added.png')


            /* Highlight Artifact Subtree (On Hold - Currently a Bug) */

            /* Hide Artifact Subtree (On Hold- Currently a Bug) */

            /* Delete Artifact (On Hold - Currently a Bug)*/

            /* Deleting the project (Add 1 to the closewindowiconbutton to every window open)*/
            .logToConsole('Deleting the project')
            .clickSelector(projectDropDownGloabl, OpenProjectButton)
            .click(deleteProjectIcon)
            .fillInTextBox(projectName, deleteingProjectInputField)
            .click(deleteProjectdeleteButton)
            .takeScreenShot(screenShotDestination + 'Project_Deletion_Successful.png')
            .assert.visible('@projectSelectionMessage', "WebAPI: Project has successfully been deleted")
            .useXpath().click(openProjectCloseWindowButton).useCss()


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