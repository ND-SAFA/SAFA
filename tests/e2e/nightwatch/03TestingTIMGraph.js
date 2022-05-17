/*********************************************************
TestingTIMGraph.js - Created by: Jeremy Arellano
    This test will test the capabilities of the TIM Graph, while
    also serving to test Nightwatch's ability to interact with 
    the TIM graph UI. This test is not guaranteed to work, but
    it is nessesary to test how the TIM graph is currently structured.

    Some Notes:
        - This is where I will put any errors or bugs that I encounter throughout the testing process.
*********************************************************/
 
module.exports = {
    '@disabled': false,
    '@tags' : ['SAFA'],
    'TIM Graph Test'(browser) {
        const page = browser.page.UI_Interaction();

        /* Our constants will go here */
        const TestDataLocation = 'tests/e2e/nightwatch/TestData/';
        const screenShotDestination = '/03TestingTIMGraph/';
        const F15Node               = `(//*[contains(text(),' F15') and @class="artifact-sub-header text-body-1"])[position()=1]`
        const rightClickMenu        = `button[id="add-artifact"]`
        const artifactViewerTitle   = `h1[class="text-h6 artifact-title"]`
        const artifactViewerDescription = `p[class="text-body-1"]`
        const centerGraphButton     = `(//*[@aria-expanded="false" and @type="button" and @class="v-btn v-btn--icon v-btn--round theme--light v-size--default secondary--text"])[4]`

        /* Our test will occur here */
        page
            /* Navigate to the TIM graph page */
            .navigate()
            .waitForElementVisible('@loginImageIcon', 5000, "WebAPI: URL loaded successfully")
            .assert.titleEquals('SAFA', 'UI: Title is correct') // Note, succsess in running the program so far
            .loginSession(screenShotDestination, 'Login_Success.png')
            .clickSelector(' Project ', ' Open Project ')
            .useXpath()
            .click(`(//*[contains(text(),' Continue ')])[last()]`)
            .useCss()
            .clickButton(' Submit ')
            

            /* Testing Elements of the TIM Graph */
            .waitForElementVisible('@timGraph', 5000, "WebAPI: TIM Graph is Visible")
            .useXpath()
            .click(centerGraphButton)
            .pause(1500)
            .waitForElementVisible(F15Node, 5000, "UI: F20 is Visible and Interactable")
            .rightClick(F15Node)
            .useCss()
            .waitForElementVisible(rightClickMenu, 5000, "UI: Right Click Menu is Visible")
            .takeScreenShot(screenShotDestination + 'F20Node.png')
            
            /* Add a new Artifact */
            /*
            .clickButton('Add Artifact')
            .fillInTextBox('New Node', 'Artifact Name')
            .clickSelector('Artifact Type', 'Hazard.csv')
            .fillInTextBox('This is a new node', 'Artifact Summary')
            .fillInTextBox('This is a new node', 'Artifact Body')
            .click('Save')
            */

            /* View Details of an Artifact */
            .clickButton('View Artifact')
            .waitForElementVisible(artifactViewerTitle, 5000, "UI: Artifact Viewer is Visible")
            .waitForElementVisible(artifactViewerDescription, 5000, "UI: Artifact Description is Visible")
            .takeScreenShot(screenShotDestination + 'ArtifactViewer.png')
            
            /* Drag and Drop an Artifact */
            .pause(1000)
            .useXpath()
            .click(centerGraphButton)
            .pause(500)
            .dragAndDrop(F15Node, {x: 100, y: 100})
            .pause(1000)
            .takeScreenShot(screenShotDestination + 'F15Node_Dragged.png')
            
            /*
            .clickAndHold(F15Node)
        
        browser
            .moveTo(null, 2432, -818 )
            .mouseButtonUp(0, "UI: F15 Dragged and Dropped")
        */
            /* End of test */
            .end();

    }
};