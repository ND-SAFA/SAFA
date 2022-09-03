Cypress.Commands.add("projectSettingsSelector", () => {
  cy.clickButtonWithName("Project").clickButtonWithName("Project Settings");
});
