import { DataCy } from "@/fixtures";

Cypress.Commands.add("switchToTimView", () => {
  cy.clickButton(DataCy.navTimButton);
});
