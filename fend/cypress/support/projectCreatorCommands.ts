import {
  DataCy,
  miniProjectFiles,
  genProjectFiles,
  Routes,
  simpleProjectFilesMap,
  testProject,
} from "@/fixtures";

const validUser = Cypress.env("validUser");

Cypress.Commands.add("initEmptyProject", () => {
  cy.dbResetJobs().dbResetProjects();

  cy.visit(Routes.PROJECT_CREATOR + "?tab=bulk")
    .login(validUser.email, validUser.password)
    .locationShouldEqual(Routes.PROJECT_CREATOR);

  cy.setProjectIdentifier("bulk")
    .clickButton(DataCy.creationEmptyToggle)
    .clickButton(DataCy.creationUploadButton);
});

Cypress.Commands.add("initProject", (waitForComplete = true, generateData) => {
  cy.dbResetJobs().dbResetProjects();

  cy.visit(Routes.PROJECT_CREATOR + "?tab=bulk")
    .login(validUser.email, validUser.password)
    .locationShouldEqual(Routes.PROJECT_CREATOR);

  cy.setProjectIdentifier("bulk")
    .uploadFiles(
      DataCy.creationBulkFilesInput,
      ...(generateData ? genProjectFiles : miniProjectFiles)
    )
    .clickButton(DataCy.creationUploadButton);

  if (!waitForComplete) return;

  cy.waitForJobLoad();
});

Cypress.Commands.add("initProjectVersion", (waitForComplete = true) => {
  cy.dbResetVersions();

  cy.visit(Routes.MY_PROJECTS)
    .login(validUser.email, validUser.password)
    .locationShouldEqual(Routes.MY_PROJECTS);

  cy.expandViewport("l")
    .projectSelectorContinue("project")
    .projectSelectorContinue("version")
    .locationShouldEqual(Routes.ARTIFACT);

  cy.getCy(DataCy.appLoading).should("not.exist");
  cy.clickButton(DataCy.navTreeButton);

  cy.waitForProjectLoad(waitForComplete);
});

Cypress.Commands.add("setProjectIdentifier", (type) => {
  if (type === "standard") {
    cy.getCy(DataCy.creationStandardNameInput).type(testProject.name);
    cy.getCy(DataCy.creationStandardDescriptionInput).type(
      testProject.description
    );
    cy.clickButton(DataCy.stepperContinueButton);
  } else if (type === "modal") {
    cy.getCy(DataCy.projectEditNameInput).type(testProject.name);
    cy.getCy(DataCy.projectEditDescriptionInput).type(testProject.description);
  } else {
    cy.getCy(DataCy.creationBulkNameInput).type(testProject.name);
    cy.getCy(DataCy.creationBulkDescriptionInput).type(testProject.description);
    cy.clickButton(DataCy.creationContinueButton);
  }
});

Cypress.Commands.add("openPanelAfterClose", () => {
  cy.wait(300).clickButton(DataCy.creationFilePanel, "last");
});

Cypress.Commands.add("createArtifactPanel", (name, file, next) => {
  cy.inputText(DataCy.creationTypeInput, name, false, true);
  cy.uploadFiles(DataCy.creationStandardFilesInput, file);

  if (next) {
    cy.clickButton(DataCy.stepperContinueButton);
  }
});

Cypress.Commands.add("createTraceMatrix", (source, target, file, next) => {
  cy.clickButton(DataCy.creationTraceSourceInput).clickButtonWithName(source);
  cy.clickButton(DataCy.creationTraceTargetInput).clickButtonWithName(target);

  if (file) {
    cy.uploadFiles(DataCy.creationStandardFilesInput, file);
  }

  if (next) {
    cy.clickButton(DataCy.stepperContinueButton);
  }
});

Cypress.Commands.add("createReqToHazardFiles", (createTraces, next) => {
  cy.setProjectIdentifier("standard");
  cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);
  cy.clickButtonWithName("New Artifact Type");
  cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard, true);

  if (createTraces) {
    cy.createTraceMatrix(
      "requirement",
      "hazard",
      simpleProjectFilesMap.requirement2hazard,
      next
    );
  }
});

Cypress.Commands.add("waitForJobLoad", () => {
  // TODO: remove this workaround once websocket messages are fixed.
  cy.wait(5000);
  // cy.wrap(null, { timeout: 10000 }).then(() => {
  //   cy.getCy(DataCy.jobOpenButton, "first", 10000).should("not.be.disabled");
  // });
});
