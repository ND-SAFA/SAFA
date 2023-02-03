import { DataCy } from "@/fixtures";

Cypress.Commands.add("openTraceApproval", () => {
  cy.expandViewport()
    .clickButtonWithName("Trace Prediction")
    .switchTab("Trace Approval")
    .clickButton(DataCy.sidebarCloseButton);
});

Cypress.Commands.add("sortTraceApproval", (sort) => {
  if (sort === "name") {
    cy.clickButton(DataCy.traceLinkTableSortByInput).type(
      "{enter}{downArrow}{enter}{esc}"
    );
  } else if (sort === "approval") {
    cy.clickButton(DataCy.traceLinkTableSortByInput).type(
      "{backspace}{upArrow}{enter}{esc}"
    );
  } else {
    cy.clickButton(DataCy.traceLinkTableSortByInput).type("{backspace}{esc}");
  }
});

Cypress.Commands.add("groupTraceApproval", (group) => {
  if (group === "type") {
    cy.clickButton(DataCy.traceLinkTableGroupByInput).type(
      "{backspace}{upArrow}{enter}{esc}"
    );
  } else if (group === "status") {
    cy.clickButton(DataCy.traceLinkTableGroupByInput).type(
      "{downArrow}{downArrow}{enter}{esc}"
    );
  } else {
    cy.clickButton(DataCy.traceLinkTableGroupByInput).type("{backspace}{esc}");
  }
});

Cypress.Commands.add("filterTraceApproval", (filter) => {
  if (filter === "approved") {
    cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
      "{backspace}{downArrow}{enter}{esc}"
    );
  } else if (filter === "declined") {
    cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
      "{backspace}{downArrow}{downArrow}{enter}{esc}"
    );
  } else {
    cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
      "{backspace}{downArrow}{enter}{downArrow}{enter}{downArrow}{enter}{esc}"
    );
  }
});
