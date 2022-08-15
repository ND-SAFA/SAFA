import { DataCy } from "../fixtures";

Cypress.Commands.add("login", (email, password) => {
  cy.inputText(DataCy.emailInput, email)
    .inputText(DataCy.passwordInput, password)
    .clickButton(DataCy.loginButton);
});

Cypress.Commands.add("logout", () => {
  cy.getCy(DataCy.accountDropdown).click().clickButton("button-logout");
});
