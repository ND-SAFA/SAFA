import { DataCy } from "../fixtures";

Cypress.Commands.add("switchToTableView", () => {
  cy.clickButton(DataCy.navToggleView);
});

Cypress.Commands.add("artifactTableFirstElementLookUp", () => {
  cy.getCy(DataCy.artifactTableArtifact).first();
});

Cypress.Commands.add("artifactTableChangeSort", (sortType: string) => {
  /* Currently does not work due to not finding element but hoping it will.
    cy.getCy(DataCy.artifactTableListItems)
      .filter(":visible")
      .contains(sortType);
    */
});

Cypress.Commands.add(
  "addTableArtifact",
  (
    name: string,
    type: string,
    docType: string,
    parentArtifact: string,
    body: string,
    summary: string
  ) => {
    cy.inputText(DataCy.artifactTableCreateArtifactNameInput, name);
    cy.clickButton(DataCy.artifactTableCreateArtifactTypeInput)
      .type("{backspace}{esc}")
      .inputText(DataCy.artifactTableCreateArtifactTypeInput, type)
      .type("{enter}");
    cy.clickButton(DataCy.artifactTableCreateArtifactParentArtifactInput)
      .type("{backspace}{esc}")
      .inputText(
        DataCy.artifactTableCreateArtifactParentArtifactInput,
        parentArtifact
      )
      .type("{downArrow}{enter}");

    cy.inputText(DataCy.artifactTableCreateArtifactBodyInput, body);
    cy.inputText(DataCy.artifactTableCreateArtifactSummaryInput, summary);
    cy.clickButton(DataCy.artifactTableCreateArtifactSaveButton);
  }
);
