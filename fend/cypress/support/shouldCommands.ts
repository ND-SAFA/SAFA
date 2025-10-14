Cypress.Commands.add("locationShouldEqual", (route) => {
  cy.location("pathname", { timeout: 10000 }).should("equal", route);
});
