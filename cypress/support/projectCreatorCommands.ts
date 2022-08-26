import { DataCy, testProject } from "../fixtures";

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

Cypress.Commands.add("createArtifactPanel", (name: string, file: string) => {
  cy.clickButton(DataCy.creationCreatePanelButton);
  cy.getCy(DataCy.creationTypeInput).type(name);
  cy.clickButton(DataCy.creationTypeButton);
  cy.uploadFiles(DataCy.creationStandardFilesInput, file);
});

Cypress.Commands.add("createTraceMatrix", (name: string, artifact: string) => {
  cy.clickButton(DataCy.stepperContinueButton);
  cy.clickButtonWithName("Create new trace matrix");
  cy.clickButtonWithName("Select source");
  cy.clickMenuOption(name);

  cy.clickButtonWithName("Select target");
  cy.clickMenuOption(artifact);
});

Cypress.Commands.add("uploadingTraceLinks", (file: string) => {
  cy.clickButtonWithName("Create trace matrix");
  cy.uploadFiles(DataCy.creationStandardFilesInput, file);
  cy.clickButton(DataCy.stepperContinueButton);
});
