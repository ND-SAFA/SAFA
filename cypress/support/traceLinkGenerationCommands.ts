import { DataCy } from "../fixtures";

Cypress.Commands.add("openApproveGeneratedTraceLinks", () => {
  cy.clickButton(DataCy.navLinksButton).clickButtonWithName(
    "Approve Generated Trace Links"
  );
});
