import { DataCy } from "../fixtures";

Cypress.Commands.add("fillArtifactModal", ({ name, type, body, parent }) => {
  if (name === undefined) name = `New ${Math.random()}`;
  if (type === undefined) type = "Designs{downArrow}{enter}";
  if (body === undefined) body = "New Artifact";

  cy.getCy(DataCy.artifactSaveModal).within(() => {
    cy.inputText(DataCy.artifactSaveNameInput, name)
      .inputText(DataCy.artifactSaveBodyInput, body)
      .inputText(DataCy.artifactSaveTypeInput, type);

    if (parent) {
      cy.inputText(DataCy.artifactSaveParentInput, parent);
    }
  });
});

Cypress.Commands.add("createNewArtifact", (props) => {
  cy.clickButton(DataCy.artifactFabToggle)
    .clickButton(DataCy.artifactFabCreateArtifact)
    .fillArtifactModal(props);
});

Cypress.Commands.add("saveArtifact", () => {
  cy.getCy(DataCy.artifactSaveModal).within(() => {
    cy.clickButton(DataCy.artifactSaveSubmitButton);
  });
});

Cypress.Commands.add("fillTraceLinkModal", (source = "", target = "") => {
  cy.getCy(DataCy.traceSaveModal).within(() => {
    cy.inputText(
      DataCy.traceSaveSourceInput,
      `${source}{downArrow}{enter}`
    ).inputText(DataCy.traceSaveTargetInput, `${target}{downArrow}{enter}`);
  });
});

Cypress.Commands.add("createNewTraceLink", (source = "", target = "") => {
  cy.clickButton(DataCy.artifactFabToggle)
    .clickButton(DataCy.artifactFabCreateTrace)
    .fillTraceLinkModal(source, target);
});

Cypress.Commands.add("saveTraceLink", () => {
  cy.getCy(DataCy.traceSaveModal).within(() => {
    cy.clickButton(DataCy.traceSaveSubmitButton);
  });
});
