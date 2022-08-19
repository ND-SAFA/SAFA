import { DataCy } from "../fixtures";

Cypress.Commands.add("openProjectSelector", () => {
  cy.clickButtonWithName("Project").clickButtonWithName("Open Project");
});

Cypress.Commands.add("projectSelectorContinue", () => {
  cy.getCy(DataCy.selectionModal).within(() => {
    cy.clickButton(DataCy.stepperContinueButton);
  });
});

Cypress.Commands.add("createNewVersion", (type) => {
  const selectors: Record<typeof type, string> = {
    major: DataCy.versionCreateMajorButton,
    minor: DataCy.versionCreateMinorButton,
    revision: DataCy.versionCreateRevisionButton,
  };

  cy.getCy(DataCy.selectionModal).within(() => {
    cy.getCy(DataCy.selectionVersionList).within(() => {
      cy.clickButton(DataCy.selectorAddButton);
    });
  });

  cy.getCy(DataCy.versionCreateModal).within(() => {
    cy.clickButton(selectors[type]);
  });
});
