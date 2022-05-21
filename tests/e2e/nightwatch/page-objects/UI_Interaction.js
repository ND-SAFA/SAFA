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
 *    - moveToElement() function is being used since there is a bug with Nightwatch 
 *      with element clicks being intercepted. This function prevents this bug from happening.
 */

module.exports = {
    '@disabled': true, // this will prevent this from being run as a test


    url: 'http://localhost:8080/',

    elements: {
        checkContinueButtonDisabled             : '.container [type="button"].v-btn--outlined',
        ProfilePictureAttributes                : 'button[type="button"][role="button"]',
        TestDataLocation                        : 'tests/e2e/nightwatch/TestData/',
        emailInputField                         : 'input[id="input-150"]',
        projectCreationSteps                    : '.v-stepper__header',
        webTitleGlobal                          : 'h1[class="text-h4 white--text ml-4"]',
        artifactCreatorWarning                  : 'div[class="col"][style="white-space: nowrap;"]',
        artifactCreatorNameWarning              : 'div[class="v-messages__message"]',
        traceLinkCreatorWarning                 : 'div[class="col"][style="white-space: nowrap;"]',
        traceLinkNoInputWarning                 : 'div[class="ma-1 pa-0 text-center white--text col col-9 align-self-center"]',
        projectSelectionMessage                 : 'td[colspan="5"]',
        projectCreationSuccessfulMessage        : 'div[class="ma-1 pa-0 text-center white--text col col-9 align-self-center"]',
        rightClickMenu                          : `button[id="add-artifact"]`,
        artifactTypeDropDown                    : `div[class="v-select__slot"] label[class="v-label theme--light"]`,
        /* Image Elements */
        loginImageIcon                          : '[src="/img/SAFA.28196e73.png"]',
        checkMarkIcon                           : 'i[aria-hidden="true"][class="v-icon notranslate mdi mdi-check theme--light success--text"]:last-child',
        errorMarkIcon                           : 'i[aria-hidden="true"][class="v-icon notranslate mdi mdi-close theme--light error--text"]:last-child',
        dropDownIcon                            : 'i[aria-hidden="true"][class="v-icon notranslate mdi mdi-chevron-down theme--light"]',
        deleteProjectIcon                       : 'i[aria-hidden="true"][class="v-icon notranslate mdi mdi-delete theme--light"]',
        closeWindowIcon                         : 'i[aria-hidden="true"][class="v-icon notranslate mdi mdi-close theme--light"]',
        
        /* Tim Graph Elements */
        timGraph                                : 'canvas[data-id="layer1-drag"]',
        zoomInButton                            : 'button[id="zoom-in"]',
        centerGraphButton                       : '(//*[@aria-expanded="false" and @type="button" and @class="v-btn v-btn--icon v-btn--round theme--light v-size--default secondary--text"])[5]',
        addArtifactButton                       : 'button[id="add-artifact"]',

    },

    commands: [ {

        fillInTextBox(textBoxValue, textBoxName) {
            /* Set the page constant */
            const page = this;
            
            const textBoxLocation = `//label[contains(text(),'${textBoxName}')]`;
            const textBoxLocationInput = `//label[contains(text(),'${textBoxName}')]/following-sibling::*[1]`;
            /* Set the text box location */
            page
                .useXpath()
                .moveToElement(textBoxLocation, undefined, undefined)
                .setValue(textBoxLocationInput, textBoxValue)
                .useCss();

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
            const page = this;
            const labelNameLocation = `(//span[contains(text(),'${lableName}')])[last()]`;

            page
                .useXpath()
                .moveToElement(labelNameLocation, undefined, undefined)
                .click(labelNameLocation)
                .useCss();

            return this;
        },
    
        loginSession(screenShotDestination, screenShotName, userName, password, useDefaultCredentials) {
            /* Set the page constant */
            const page = this;

            if (!useDefaultCredentials) {
                userName = 'tester@test.com';             // Remove these once account deletion is added
                password = '\\+sX,^]ptK~-"4vn';
            }

            /* Login to the website */
            page
                .fillInTextBox(userName, 'Email')
                .buttonNotClickable('Login', "UI: Login button is disabled without a valid password entered")
                .fillInTextBox(password, 'Password')
                .clickButton('Login')
                .waitForElementVisible('@ProfilePictureAttributes', 2000, "UI: Profile picture is visible after login")
                .takeScreenShot(screenShotDestination + screenShotName)
                .useCss();
            /* Return the page object */
            return this;

        },

        uploadFileWithParameters(fileLocation, fileName) {
            const page = this;
            const fileUploadLocation = `(//*[contains(text(),'File')]/following-sibling::input)[last()]`;
            page
                .useXpath()
                .moveToElement(fileUploadLocation, undefined, undefined)
                .uploadFile(fileUploadLocation, require('path').resolve(fileLocation + fileName))
                .useCss()

            return this;
        },

        clickSelector(selectorName, selectorValue) {
            const page = this;
            const selectorValueLocation  = `(//*[contains(text(),'${selectorValue}') and @class="v-btn__content" ])[last()]`;

            page
                .clickButton(selectorName)
                .useXpath()
                .moveToElement(selectorValueLocation, undefined, undefined)
                .click(selectorValueLocation)
                .useCss();
            return this;
        },

        clickSelectorTraceLinks(sourceName, targetName) {
            const page = this;

            /* Element Names */
            const createNewTraceLinkButton      = 'Create new trace matrix';
            const sourceTraceLinkButton         = ' Select Source ';
            const targetTraceLinkButton         = ' Select Target ';
            const createTraceLinkButton         = 'Create Trace Matrix ';
            /* Xpaths */
            const sourceOptionXpath             = `//*[contains(text(),'${sourceName}') and @class="v-btn__content" ]`;
            const targetOptionXpath             = `(//*[contains(text(),'${targetName}') and @class="v-btn__content" ])[last()]`;
            page
                .clickButton(createNewTraceLinkButton)
                .clickButton(sourceTraceLinkButton)
                .useXpath()
                .moveToElement(sourceOptionXpath, undefined, undefined)
                .click(sourceOptionXpath)
                .clickButton(targetTraceLinkButton)
                .useXpath()
                .moveToElement(targetOptionXpath, undefined, undefined)
                .click(targetOptionXpath)
                .clickButton(createTraceLinkButton)
                .useCss();
            
            return this;
        },

        buttonNotClickable(buttonName, message) {
            /* NOTE: This function uses a REGEX expression to find the element "true" */
            const page = this;
            const buttonLocation = `//*[contains(text(),'` + buttonName + `')]/parent::button`;
            page
                .useXpath()
                .expect.element(buttonLocation)
                .to.have.property('disabled', message)
                .matches(/true\b/);
            
            page.useCss();
            
            return this;
        },

        buttonClickable(buttonName, message) {
            /* NOTE: This function uses a REGEX expression to find the element "true" */
            const page = this;
            const buttonLocation = `//*[contains(text(),'` + buttonName + `')]/parent::button`;
            page
                .useXpath()
                .expect.element(buttonLocation)
                .to.have.property('disabled', message)
                .matches(/false\b/);
            
            page.useCss();
            
            return this;
        },

        logToConsole(message) {
            const page = this;

            page
                .perform(function() {
                    console.log(message);
                });
            
            return this;
        },

        checkText(textName, message) {
            const page = this;
            const elementLocation = `//*[contains(text(),'` + textName + `')]`;
            page
                .useXpath()
                .assert.visible(elementLocation, message);
            
            page.useCss();

            return this;
        },

        checkUploadSuccess(message) {
            const page = this;
            const checkMarkIcon = `(.//div//i[@aria-hidden="true"][@class="v-icon notranslate mdi mdi-check theme--light success--text"])[last()]`

            page    
                .useXpath()
                .assert.visible(checkMarkIcon, message)
                .useCss();

            return this;
        },

        checkUploadFailure(message) {
            const page = this;
            const checkMarkIcon = `(.//div//i[@aria-hidden="true"][@class="v-icon notranslate mdi mdi-close theme--light error--text"])[last()]`

            page
                .useXpath()
                .expect.element(checkMarkIcon)
                .to.be.visible

                .assert.not.visible(checkMarkIcon, message)
                .useCss();

            return this;
        },

        findAndTestTIMNode(nodeName, TIMNodelocation, suppressOutput, message) {
            const page = this;
            const nodeLocation = `(//span[contains(text(), '${nodeName}') and @class="artifact-sub-header text-body-1"])[position()=1]`
            TIMNodelocation[nodeName] = nodeLocation;
            
            page.useXpath();
            
            if (!suppressOutput) {
                page.assert.visible(nodeLocation, message);
            }

            page.useCss();

            return this;
        }

    }]

};

