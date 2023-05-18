import { DataCy } from "@/fixtures";

Cypress.Commands.add("sortTraceApproval", (sort) => {
  if (sort === "name") {
    cy.clickButton(DataCy.traceLinkTableSortByInput).clickMenuOption("name");
  } else if (sort === "approval") {
    cy.clickButton(DataCy.traceLinkTableSortByInput).clickMenuOption(
      "approval"
    );
  } else {
    cy.clickButton(DataCy.traceLinkTableSortByInput).type("{backspace}{esc}");
  }
});

Cypress.Commands.add("groupTraceApproval", (group) => {
  if (group === "type") {
    cy.clickButton(DataCy.traceLinkTableGroupByInput).clickMenuOption("type");
  } else if (group === "status") {
    cy.clickButton(DataCy.traceLinkTableGroupByInput).clickMenuOption("status");
  } else {
    cy.clickButton(DataCy.traceLinkTableGroupByInput).type("{backspace}{esc}");
  }
});

Cypress.Commands.add("filterTraceApproval", (filter) => {
  if (filter === "approved") {
    cy.clickButton(DataCy.traceLinkTableApprovalInput).type(
      "{backspace}approved{downArrow}{enter}"
    );
  } else if (filter === "declined") {
    cy.clickButton(DataCy.traceLinkTableApprovalInput).type(
      "{backspace}declined{downArrow}{enter}"
    );
  } else {
    cy.clickButton(DataCy.traceLinkTableApprovalInput).type("{backspace}{esc}");
  }
});
