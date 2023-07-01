import { DataCy } from "@/fixtures";

Cypress.Commands.add("switchToTableView", (tab) => {
  cy.clickButton(DataCy.navTableButton);

  if (tab === "trace") {
    cy.switchTab("Trace Links");
  } else if (tab === "approval") {
    cy.switchTab("Trace Approval");
  }
});

Cypress.Commands.add("sortArtifactTable", (sort) => {
  if (sort === "name") {
    cy.clickButton(DataCy.artifactTableSortByInput).clickMenuOption("name");
  } else if (sort === "type") {
    cy.clickButton(DataCy.artifactTableSortByInput).clickMenuOption("type");
  } else {
    cy.clickButton(DataCy.artifactTableSortByInput).type("{backspace}{esc}");
  }
});

Cypress.Commands.add("groupArtifactTable", (group) => {
  if (group === "name") {
    cy.clickButton(DataCy.artifactTableGroupByInput).clickMenuOption("name");
  } else if (group === "type") {
    cy.clickButton(DataCy.artifactTableGroupByInput).clickMenuOption("type");
  } else {
    cy.clickButton(DataCy.artifactTableGroupByInput).type("{backspace}{esc}");
  }
});

Cypress.Commands.add("filterTraceMatrixTable", (row, col) => {
  cy.clickButton(DataCy.traceMatrixTableRowTypeInput).type(
    `${row}{downArrow}{enter}{esc}`
  );

  cy.clickButton(DataCy.traceMatrixTableColTypeInput).type(
    `${col}{downArrow}{enter}{esc}`
  );
});
