Cypress.Commands.add("openProjectSelector", () => {
  cy.clickButtonWithName("Project").clickButtonWithName("Open Project");
});
