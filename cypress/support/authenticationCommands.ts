Cypress.Commands.add("login", (email, password) => {
  cy.inputText("input-email", email)
    .inputText("input-password", password)
    .clickButton("button-login");
});

Cypress.Commands.add("logout", () => {
  cy.getCy("account-dropdown").click().clickButton("button-logout");
});
