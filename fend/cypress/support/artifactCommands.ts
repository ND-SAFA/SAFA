import { DataCy } from "@/fixtures";

Cypress.Commands.add("fillArtifactFields", ({ name, type, body, parent }) => {
  if (name === undefined) name = `New ${Math.random()}`;
  if (type === undefined) type = "Design{downArrow}{enter}";
  if (body === undefined) body = "New Artifact";

  cy.inputText(DataCy.artifactSaveNameInput, name)
    .inputText(DataCy.artifactSaveBodyInput, body)
    .inputText(DataCy.artifactSaveTypeInput, type);

  if (parent) {
    cy.inputText(DataCy.artifactSaveParentInput, parent);
  }
});

Cypress.Commands.add("createNewArtifact", (props, save, close) => {
  cy.clickButton(DataCy.artifactFabToggle)
    .clickButton(DataCy.artifactFabCreateArtifact)
    .fillArtifactFields(props);

  if (!save) return;

  cy.clickButton(DataCy.artifactSaveSubmitButton);

  if (!close) return;

  cy.getCy(DataCy.snackbarSuccess).should("be.visible");
  cy.clickButton(DataCy.selectedPanelCloseButton);
});
