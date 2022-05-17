/******************************************************
 * UI_Interaction.js - Created by: Jeremy Arellano
 *    This is a page objects file that will store all
 *    of the elements that will be used in the UI, as well as commonly 
 *    used functions.
 * 
 *  Some Notes:
 *     - This file is currently being used in the tests
 *      folder.
 *    - This objects file will constantly evolve as more functions are simplified
 */

module.exports = {
    '@disabled': true, // this will prevent this from being run as a test


    url: 'http://localhost:8080/',

    elements: {
        loginImageIcon                          : '[src="/img/SAFA.28196e73.png"]',
        checkProjectNumberSteps                 : '.v-stepper__header',
        checkContinueButtonDisabled             : '.container [type="button"].v-btn--outlined',
        ProfilePictureAttributes                : 'button[type="button"][role="button"]',
        TestDataLocation                        : 'tests/e2e/nightwatch/TestData/',
        HazardsUploadButton                     : '#input-162[type="file"]',
        RequirementsUploadButton                : '#input-199[type="file"]',
        DesignsUploadButton                     : '#input-236[type="file"]',
        EnvironmentalAssumptionsUploadButton    : '#input-273[type="file"]',
        Requirement2HazardsUploadButton         : '#input-346[type="file"]',
        Environmental2HazardsUploadButton       : '#input-411[type="file"]',

        /* Tim Graph Elements */
        timGraph                                : 'canvas[data-id="layer1-drag"]',
        zoomInButton                            : 'button[id="zoom-in"]',
        centerGraphButton                       : `(//*[@aria-expanded="false" and @type="button" and @class="v-btn v-btn--icon v-btn--round theme--light v-size--default secondary--text"])[5]`,
        

    },

    commands: [ {
        fillInTextBox(textBoxValue, textBoxName) {
            /* Set the page constant */
            const page = this;
            
            /* Set the text box location */
            page
                .useXpath()
                .assert.visible(`//*[contains(text(),'${textBoxName}')]`, results => {
                    if (results.value) {
                        const textBoxLocation = `//*[contains(text(),'${textBoxName}')]/following-sibling::input`;
                        page.setValue( textBoxLocation, textBoxValue);
                        page.useCss();
                        page.pause(100)
                        return "UI: {textBoxName} is visible";
                    } else {
                        page.useCss();
                        return "UI: {textBoxName} is not visible";
                    }
                });

            /* Return the page object */
            return this;
        },

        takeScreenShot(screenShotName) {
            /* Set the page constant */
            const page = this;

            /* Take the screenshot */
            page
                .saveScreenshot(`tests/e2e/nightwatch/screenshots/CreateProject/${screenShotName}`);

            /* Return the page object */
            return this;
        },

        clickButton(lableName) {
            /* Set the page constant */
            const page = this;

            /* Set the button location */
            page
                .useXpath()
                .assert.visible(`//*[contains(text(),'${lableName}')]`, results => {
                    if (results.value) {
                        /* Click the button */
                        page.pause(500)
                        page.click(`//*[contains(text(),'${lableName}')]`);
                        page.pause(500);
                        page.useCss();
                        results = "UI: {lableName} is visible";
                    } else {
                        page.useCss();
                        results = "UI: {lableName} is not visible";
                    }
                });
            /* Return the page object */
            return this;
        },
    
        loginSession(screenShotDestination, screenShotName) {
            /* Set the page constant */
            const page = this;
            const userName = 'tester@test.com';
            const password = '\\+sX,^]ptK~-"4vn';

            /* Login to the website */
            page
                .fillInTextBox(userName, 'Email')
                .fillInTextBox(password, 'Password')
                .clickButton('Login')
                .waitForElementVisible('@ProfilePictureAttributes', 2000, "UI: Profile Picture is visible")
                .takeScreenShot(screenShotDestination + screenShotName);

            /* Return the page object */
            return this;

        },

        uploadFileWithParameters(fileLocation, fileName) {
            const page = this;

            page
                .useXpath()
                .uploadFile(`(//*[contains(text(),'File')]/following-sibling::input)[last()]`, require('path').resolve(fileLocation + fileName))
                .useCss();

            return this;
        },

        clickSelector(selectorName, selectorValue) {
            const page = this;

            page
                .clickButton(selectorName)
                .pause(500)
                .useXpath()
                .click(`(//*[contains(text(),'${selectorValue}') and @class="v-btn__content" ])[last()]`)
                .useCss()
                .pause(500)
            return this;
        },

        clickSelectorButton(sourceName, targetName) {
            const page = this;

            page
                .clickButton(' Create new trace matrix')
                .clickButton(' Select Source ')
                .useXpath()
                .click(`//*[contains(text(),'${sourceName}') and @class="v-btn__content" ]`)
                .clickButton(' Select Target ')
                .useXpath()
                .click(`(//*[contains(text(),'${targetName}') and @class="v-btn__content" ])[last()]`)
                .clickButton(' Create Trace Matrix ')
                .useCss()
                .pause(1000)
            return this;
        }

    }]

};

