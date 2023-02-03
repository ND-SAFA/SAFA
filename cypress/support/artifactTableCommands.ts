import { DataCy } from "@/fixtures";

Cypress.Commands.add("switchToTableView", () => {
  cy.clickButton(DataCy.navTableButton);
});
