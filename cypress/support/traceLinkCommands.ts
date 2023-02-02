import { DataCy } from "@/fixtures";

Cypress.Commands.add("fillTraceLinkFields", (source = "", target = "") => {
  cy.inputText(
    DataCy.traceSaveSourceInput,
    `${source}{downArrow}{enter}`
  ).inputText(DataCy.traceSaveTargetInput, `${target}{downArrow}{enter}`);
});

Cypress.Commands.add("createNewTraceLink", (source = "", target = "", save) => {
  cy.clickButton(DataCy.artifactFabToggle)
    .clickButton(DataCy.artifactFabCreateTrace)
    .fillTraceLinkFields(source, target);

  if (!save) return;

  cy.clickButton(DataCy.traceSaveSubmitButton);
});
