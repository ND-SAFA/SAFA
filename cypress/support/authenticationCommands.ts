Cypress.Commands.add("login", (email, password) => {
  cy.inputText("Email", email)
    .inputText("Password", password)
    .clickButton("Login");
});

Cypress.Commands.add("logout", () => {
  cy.get("#account-dropdown").click().clickButton("Logout");
});
