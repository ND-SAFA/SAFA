import { DataCy } from "@/fixtures";

Cypress.Commands.add("switchToTableView", () => {
  cy.clickButtonWithName("table");
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
