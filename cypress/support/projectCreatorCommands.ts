import { DataCy, testProject } from "../fixtures";

Cypress.Commands.add("setProjectIdentifier", (type) => {
  if (type === "standard") {
    cy.getCy(DataCy.creationStandardNameInput).type(testProject.name);
    cy.getCy(DataCy.creationStandardDescriptionInput).type(
      testProject.description
    );
  } else if (type === "modal") {
    cy.getCy(DataCy.selectionNameInput).type(testProject.name);
    cy.getCy(DataCy.selectionDescriptionInput).type(testProject.description);
  } else {
    cy.getCy(DataCy.creationBulkNameInput).type(testProject.name);
    cy.getCy(DataCy.creationBulkDescriptionInput).type(testProject.description);
  }
});

// TODO: finish
// Cypress.Commands.add("selectForPossibleErros", (containsErros: boolean) => {});
