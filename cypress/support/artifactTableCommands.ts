import { DataCy } from "@/fixtures";

Cypress.Commands.add("switchToTableView", (tab) => {
  cy.clickButton(DataCy.navTableButton);

  if (tab === "trace") {
    cy.switchTab("Trace Links");
  }
});

Cypress.Commands.add("sortArtifactTable", (sort) => {
  if (sort === "name") {
    cy.clickButton(DataCy.artifactTableSortByInput).type("{enter}{enter}{esc}");
  } else if (sort === "type") {
    cy.clickButton(DataCy.artifactTableSortByInput).type(
      "{enter}{downArrow}{enter}{esc}"
    );
  } else {
    cy.clickButton(DataCy.artifactTableSortByInput).type(
      "{backspace}{backspace}{backspace}{backspace}{esc}"
    );
  }
});

Cypress.Commands.add("groupArtifactTable", (group) => {
  if (group === "name") {
    cy.clickButton(DataCy.artifactTableGroupByInput).type(
      "{upArrow}{enter}{esc}"
    );
  } else if (group === "type") {
    cy.clickButton(DataCy.artifactTableGroupByInput).type(
      "{enter}{enter}{esc}"
    );
  } else {
    cy.clickButton(DataCy.artifactTableGroupByInput).type(
      "{backspace}{backspace}{backspace}{backspace}{esc}"
    );
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
