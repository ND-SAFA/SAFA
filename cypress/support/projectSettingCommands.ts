import { DataCy } from "../fixtures";

Cypress.Commands.add("openProjectSettings", () => {
  cy.clickButtonWithName("Project").clickButtonWithName("Project Settings");
});

Cypress.Commands.add("projectAddNewMember", (name, projectRole) => {
  cy.clickButton(DataCy.selectorAddButton);
  cy.getCy(DataCy.projectSettingsAddEmail).type(name);
  cy.getCy(DataCy.projectSettingsAddRole)
    .click({ force: true })
    .type(projectRole, { force: true })
    .type("{enter}", { force: true });
  cy.clickButton(DataCy.projectSettingsAddToProject);
});
