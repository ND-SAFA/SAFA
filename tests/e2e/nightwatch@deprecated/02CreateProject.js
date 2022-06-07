/* eslint-disable prettier/prettier */
/*************************************************************************************************************
CreateProject.js - Created by: Jeremy Arellano
    This test will create a project from the project creator and verify that it has succsessfully
    created a project. Throughout the test, Nightwatch will verify that no errors occur durring the process,
    and that the user has succsessfully reached the TIM graph page.

    Some Notes:
        - This is where I will put any errors or bugs that I encounter throughout the testing process.
***********************************************************************************************************/

module.exports = {
  "@disabled": true,
  "@tags": ["SAFA"],
  "Create Project Test"(browser) {
    const page = browser.page.UI_Interaction();

    /* Our constants will go here */
    const projectCreatorButtonName = "Continue";
    const HazardsFileName = "Hazard.csv";
    const TestDataLocation = "tests/e2e/test-data/";
    const screenShotDestination = "/02CreateProject/";

    /* Our test will occur here */
    page
      .navigate()
      .waitForElementVisible(
        "@loginImageIcon",
        5000,
        "WebAPI: URL loaded successfully"
      )
      .assert.titleEquals("SAFA", "UI: Title is correct") // Note, succsess in running the program so far
      .loginSession(screenShotDestination, "Login_Success.png")

      .fillInTextBox("SAFA", "Project Name")
      .fillInTextBox("Safety Artifact Forest Analysis", "Project description")
      .takeScreenShot(screenShotDestination + "ProjectNameEntered.png")
      .clickButton(projectCreatorButtonName)
      .takeScreenShot(screenShotDestination + "ProjectFileUpload.png")

      /* Now lets test if we can succsesfully upload a file for Hazards */
      .clickButton(" Create new artifact")
      .fillInTextBox("Hazards", "Artifact Name")
      .clickButton(" Create Artifact ")
      .takeScreenShot(screenShotDestination + "ArtifactUploadScreen.png")
      .uploadFileWithParameters(TestDataLocation, HazardsFileName)
      .pause(1000)

      .clickButton(" Create new artifact")
      .fillInTextBox("Requirements", "Artifact Name")
      .clickButton(" Create Artifact ")
      .uploadFileWithParameters(TestDataLocation, "Requirement.csv")
      .pause(1000)

      .clickButton(" Create new artifact")
      .fillInTextBox("Designs", "Artifact Name")
      .clickButton(" Create Artifact ")
      .uploadFileWithParameters(TestDataLocation, "Design.csv")
      .pause(1000)

      .clickButton(" Create new artifact")
      .fillInTextBox("Environmental Assumptions", "Artifact Name")
      .clickButton(" Create Artifact ")
      .uploadFileWithParameters(TestDataLocation, "EnvironmentalAssumption.csv")
      .pause(1000)

      .clickButton(projectCreatorButtonName)
      .pause(500)
      .takeScreenShot(
        screenShotDestination + "Artifacts_Successfully_Uploaded.png"
      )

      /***************** Now lets upload the Trace Links ****************************/
      .clickSelectorTraceLink("Requirements", "Hazards")
      .uploadFileWithParameters(TestDataLocation, "Requirement2Hazard.csv")
      .useXpath()
      .click(`(//*[contains(text(),'Generate Trace Links')])[last()]`)

      .clickSelectorTraceLink(" Environmental Assumptions ", " Hazards ")
      .uploadFileWithParameters(
        TestDataLocation,
        "EnvironmentalAssumption2Hazard.csv"
      )
      .useXpath()
      .click(`(//*[contains(text(),'Generate Trace Links')])[last()]`)

      .clickSelectorTraceLink(" Designs ", " Designs ")
      .uploadFileWithParameters(TestDataLocation, "Design2Design.csv")
      .useXpath()
      .click(`(//*[contains(text(),'Generate Trace Links')])[last()]`)

      .clickSelectorTraceLink(" Requirements ", " Requirements ")
      .uploadFileWithParameters(TestDataLocation, "Requirement2Requirement.csv")
      .useXpath()
      .click(`(//*[contains(text(),'Generate Trace Links')])[last()]`)

      .clickSelectorTraceLink(" Hazards ", " Hazards ")
      .uploadFileWithParameters(TestDataLocation, "Hazard2Hazard.csv")
      .useXpath()
      .click(`(//*[contains(text(),'Generate Trace Links')])[last()]`)

      .clickButton(projectCreatorButtonName)
      .pause(1000)
      .takeScreenShot(
        screenShotDestination + "TraceLinks_Successfully_Uploaded.png"
      )

      .clickButton(" Create Project ")

      /* End Test */
      .end();
  },
};
