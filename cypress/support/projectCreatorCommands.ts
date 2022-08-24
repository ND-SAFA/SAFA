import { DataCy, testProject } from "../fixtures";

Cypress.Commands.add("setProjectIdentifier", (type) => {
  if (type === "standard") {
    cy.getCy(DataCy.creationStandardNameInput).type(testProject.name);
    cy.getCy(DataCy.creationStandardDescriptionInput).type(
      testProject.description
    );
    cy.clickButton(DataCy.stepperContinueButton);
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
