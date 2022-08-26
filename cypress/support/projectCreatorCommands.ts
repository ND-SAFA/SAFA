import { DataCy, simpleProjectFilesMap, testProject } from "../fixtures";

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

Cypress.Commands.add("createTraceMatrix", (name, artifact, file, next) => {
  cy.clickButtonWithName("Create new trace matrix");
  cy.clickButtonWithName("Select source");
  cy.clickMenuOption(name);
  cy.clickButtonWithName("Select target");
  cy.clickMenuOption(artifact);
  cy.clickButtonWithName("Create trace matrix");

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
