import { DataCy } from "../fixtures";

Cypress.Commands.add("openProjectSelector", () => {
  cy.visit("/open")
    .location("pathname", { timeout: 2000 })
    .should("equal", "/open");
});

Cypress.Commands.add("openUploadFiles", () => {
  cy.clickButton(DataCy.navVersionButton).clickButtonWithName(
    "Upload Flat Files"
  );
});

Cypress.Commands.add("projectSelectorContinue", () => {
  cy.clickButton(DataCy.stepperContinueButton);
});

Cypress.Commands.add("createNewVersion", (type) => {
  const selectors: Record<typeof type, string> = {
    major: DataCy.versionCreateMajorButton,
    minor: DataCy.versionCreateMinorButton,
    revision: DataCy.versionCreateRevisionButton,
  };

  cy.getCy(DataCy.selectionVersionList).within(() => {
    cy.clickButton(DataCy.selectorAddButton);
  });

  cy.getCy(DataCy.versionCreateModal).within(() => {
    cy.clickButton(selectors[type]);
  });
});
