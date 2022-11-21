import { DataCy } from "../fixtures";

Cypress.Commands.add("login", (email, password) => {
  cy.inputText(DataCy.emailInput, email)
    .inputText(DataCy.passwordInput, password)
    .clickButton(DataCy.loginButton);
});

Cypress.Commands.add("logout", () => {
  cy.wait(1000)
    .getCy(DataCy.accountPage)
    .click()
    .location("pathname", { timeout: 2000 })
    .should("equal", "/account")
    .clickButton(DataCy.logoutButton);
});

Cypress.Commands.add("createNewAccount", (email, password) => {
  cy.inputText(DataCy.newAccountEmailInput, email)
    .inputText(DataCy.newAccountPasswordInput, password)
    .clickButton(DataCy.createAccountButton)
    .clickButton(DataCy.createAccountLoginButton);
});
