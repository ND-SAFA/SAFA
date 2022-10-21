import {
  DataCy,
  miniProjectFiles,
  simpleProjectFilesMap,
  testProject,
} from "../fixtures";
import { validUser } from "../fixtures/data/user.json";

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
  }
});

Cypress.Commands.add("createBulkProject", () => {
  cy.visit("/create?tab=bulk")
    .location("pathname", { timeout: 2000 })
    .should("equal", "/create");

  cy.setProjectIdentifier("bulk")
    .uploadFiles(DataCy.creationBulkFilesInput, ...miniProjectFiles)
    .clickButton(DataCy.creationUploadButton);
});

Cypress.Commands.add("openPanelAfterClose", () => {
  // Wait is required for waiting until the close animation completes.
  cy.wait(200).clickButton(DataCy.creationFilePanel, "last");
});

Cypress.Commands.add("createArtifactPanel", (name, file, next) => {
  cy.clickButton(DataCy.creationCreatePanelButton);
  cy.getCy(DataCy.creationTypeInput).type(name);
  cy.clickButton(DataCy.creationTypeButton);
  cy.uploadFiles(DataCy.creationStandardFilesInput, file);

  if (next) {
    cy.clickButton(DataCy.stepperContinueButton);
  }
});

Cypress.Commands.add("createTraceMatrix", (source, target, file, next) => {
  cy.clickButtonWithName("Create new trace matrix")
    .clickSelectOption(DataCy.creationTraceSourceInput, source)
    .clickSelectOption(DataCy.creationTraceTargetInput, target)
    .clickButton(DataCy.creationTraceCreateButton);

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

Cypress.Commands.add("loadNewProject", () => {
  cy.visit("/create")
    .login(validUser.email, validUser.password)
    .location("pathname", { timeout: 5000 })
    .should("equal", "/create");

  cy.createBulkProject()
    .getCy(DataCy.jobStatus, "first", 20000)
    .should("contain.text", "Completed");

  cy.logout();
});

Cypress.Commands.add("createProjectSettings", () => {
  cy.visit("/create")
    .login(validUser.email, validUser.password)
    .location("pathname", { timeout: 5000 })
    .should("equal", "/create");

  cy.createBulkProject()
    .getCy(DataCy.jobStatus, "first", 20000)
    .should("contain.text", "Completed");
  cy.clickButtonWithName("View Project")
    .clickButton(DataCy.navProjectButton)
    .clickButtonWithName("Project Settings");
});
