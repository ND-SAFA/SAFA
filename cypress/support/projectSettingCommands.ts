import { DataCy } from "@/fixtures";

Cypress.Commands.add("openProjectSettings", () => {
  cy.clickButton(DataCy.navSettingsButton);
});

Cypress.Commands.add("projectAddNewMember", (name, projectRole) => {
  cy.clickButton(DataCy.selectorAddButton);

  cy.inputText(DataCy.projectSettingsAddEmail, name);

  cy.clickButton(DataCy.projectSettingsAddRole).clickButtonWithName(
    projectRole
  );

  cy.clickButton(DataCy.projectSettingsAddToProject);
});
