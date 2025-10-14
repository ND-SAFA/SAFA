import { DataCy, Routes } from "@/fixtures";

Cypress.Commands.add("login", (email, password) => {
  cy.inputText(DataCy.emailInput, email, true)
    .inputText(DataCy.passwordInput, password, true)
    .clickButton(DataCy.loginButton);
});

Cypress.Commands.add("loginToPage", (email, password, route, query = {}) => {
  const queryString =
    Object.keys(query).length > 0
      ? "?" + new URLSearchParams(query).toString()
      : "";

  cy.visit(route + queryString)
    .login(email, password)
    .locationShouldEqual(route);
});

Cypress.Commands.add("logout", () => {
  cy.wait(1000)
    .clickButton(DataCy.accountPage)
    .locationShouldEqual(Routes.ACCOUNT)
    .clickButton(DataCy.logoutButton);
});

Cypress.Commands.add("createNewAccount", (email, password) => {
  cy.dbDeleteUser(email, password);

  cy.visit(Routes.CREATE_ACCOUNT)
    .inputText(DataCy.newAccountEmailInput, email)
    .inputText(DataCy.newAccountPasswordInput, password)
    .clickButton(DataCy.createAccountButton);
});
