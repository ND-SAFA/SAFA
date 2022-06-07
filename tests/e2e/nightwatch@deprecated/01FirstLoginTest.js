/* eslint-disable prettier/prettier */
/**********************************************************
FirstLoginTest.js - Created by: Jeremy Arellano
    This simple test will automate the login process and
    verify that it has succsessfully reached the create
    project screen. After the test is complete, the test will then logout and
    test if the logout process has succsessfully reached the login screen.

    Some Notes:
        - Another Bug, I am not sure why but our tests for the button and input fields will
            spit out the text field name instead of the text field value.  I am not sure why it is doing 
            this but I will try to fix it.
***********************************************************/

module.exports = {
  "@disabled": true,
  "@tags": ["SAFA"],
  "Test 01: Login and Logoff Attempt"(browser) {
    /* Set the page constant */
    const page = browser.page.UI_Interaction();

    const screenShotDestination = "/01FirstLoginTest/";

    /* Our test will occur here */
    page
      /* Login to our account */
      .navigate()
      .waitForElementVisible(
        "@loginImageIcon",
        1000,
        "UI: Front Page has loaded correctly"
      ) // Wait for the page to load
      .assert.titleEquals("SAFA", "UI: Title is correct")
      .loginSession(screenShotDestination, "Login_Success.png")

      /* Now lets test some elements on the page */
      .assert.urlContains(
        "http://localhost:8080/",
        "Param: URL has changed to display the project creator"
      )
      .assert.visible(
        "@checkProjectNumberSteps",
        "UI: Project Number Steps is visible"
      )
      .assert.attributeEquals(
        "@checkContinueButtonDisabled",
        "enabled",
        null,
        "UI: Button is disabled"
      )
      .assert.visible(
        "@ProfilePictureAttributes",
        "UI: Profile Picture is visible"
      )
      .click("@ProfilePictureAttributes")
      .takeScreenShot("Logout_Visibility.png")
      .useXpath()
      .waitForElementVisible(
        '//*[contains(text(), "Login")]',
        1000,
        "UI: Login Button is visible"
      )
      .useCss()
      .takeScreenShot("Logout_Visibility.png")

      /* End of test */
      .end();
  },
};
