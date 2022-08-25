import { DataCy } from "../fixtures";

Cypress.Commands.add("createNewArtifact", (name, type, description) => {
  if (name === undefined) name = `New ${Math.random()}`;
  if (type === undefined) type = "Designs{downArrow}{enter}";
  if (description === undefined) description = "New Artifact";

  cy.clickButton(DataCy.artifactFabToggle).clickButton(
    DataCy.artifactFabCreateArtifact
  );

  cy.getCy(DataCy.artifactSaveModal).within(() => {
    cy.inputText(DataCy.artifactSaveNameInput, name);
    cy.inputText(DataCy.artifactSaveBodyInput, description);
    cy.inputText(DataCy.artifactSaveTypeInput, type);
  });
});
