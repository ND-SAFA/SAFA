import { DataCy } from "../fixtures";

Cypress.Commands.add("projectSettingsSelector", () => {
  cy.clickButtonWithName("Project").clickButtonWithName("Project Settings");
});

Cypress.Commands.add("addingNewMember", (name, projectRole) => {
  cy.clickButton(DataCy.selectorAddButton);
  cy.getCy(DataCy.projectSettingsAddEmail).type(name);
  cy.clickButtonWithName("Project Role");
  cy.clickButtonWithName(projectRole);
});
