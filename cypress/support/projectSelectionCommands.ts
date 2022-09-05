Cypress.Commands.add("openProjectSelector", () => {
  cy.clickButtonWithName("Project").clickButtonWithName("Open Project");
});

Cypress.Commands.add("projectSettingsSelector", () => {
  cy.clickButtonWithName("Project").clickButtonWithName("Project Settings");
});
