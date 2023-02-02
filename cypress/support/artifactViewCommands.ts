import { DataCy } from "@/fixtures";

Cypress.Commands.add("fillArtifactModal", ({ name, type, body, parent }) => {
  if (name === undefined) name = `New ${Math.random()}`;
  if (type === undefined) type = "Designs{downArrow}{enter}";
  if (body === undefined) body = "New Artifact";

  cy.inputText(DataCy.artifactSaveNameInput, name)
    .inputText(DataCy.artifactSaveBodyInput, body)
    .inputText(DataCy.artifactSaveTypeInput, type);

  if (parent) {
    cy.inputText(DataCy.artifactSaveParentInput, parent);
  }
});

Cypress.Commands.add("createNewArtifact", (props, save) => {
  cy.clickButton(DataCy.artifactFabToggle)
    .clickButton(DataCy.artifactFabCreateArtifact)
    .fillArtifactModal(props);

  if (!save) return;

  cy.clickButton(DataCy.artifactSaveSubmitButton);
});

Cypress.Commands.add("saveArtifact", () => {
  cy.clickButton(DataCy.artifactSaveSubmitButton);
});

Cypress.Commands.add("fillTraceLinkModal", (source = "", target = "") => {
  cy.inputText(
    DataCy.traceSaveSourceInput,
    `${source}{downArrow}{enter}`
  ).inputText(DataCy.traceSaveTargetInput, `${target}{downArrow}{enter}`);
});

Cypress.Commands.add("createNewTraceLink", (source = "", target = "", save) => {
  cy.clickButton(DataCy.artifactFabToggle)
    .clickButton(DataCy.artifactFabCreateTrace)
    .fillTraceLinkModal(source, target);

  if (!save) return;

  cy.clickButton(DataCy.traceSaveSubmitButton);
});

Cypress.Commands.add("saveTraceLink", () => {
  cy.clickButton(DataCy.traceSaveSubmitButton);
});
