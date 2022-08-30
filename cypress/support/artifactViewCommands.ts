import { DataCy } from "../fixtures";

Cypress.Commands.add("fillArtifactModal", (name, type, description) => {
  if (name === undefined) name = `New ${Math.random()}`;
  if (type === undefined) type = "Designs{downArrow}{enter}";
  if (description === undefined) description = "New Artifact";

  cy.getCy(DataCy.artifactSaveModal).within(() => {
    cy.inputText(DataCy.artifactSaveNameInput, name);
    cy.inputText(DataCy.artifactSaveBodyInput, description);
    cy.inputText(DataCy.artifactSaveTypeInput, type);
  });
});

Cypress.Commands.add("createNewArtifact", (name, type, description) => {
  cy.clickButton(DataCy.artifactFabToggle).clickButton(
    DataCy.artifactFabCreateArtifact
  );

  cy.fillArtifactModal(name, type, description);
});

Cypress.Commands.add("saveArtifact", () => {
  cy.getCy(DataCy.artifactSaveModal).within(() => {
    cy.clickButton(DataCy.artifactSaveSubmitButton);
  });
});
