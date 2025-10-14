import { DataCy, Routes } from "@/fixtures";

Cypress.Commands.add("openProjectSelector", () => {
  cy.visit(Routes.MY_PROJECTS).locationShouldEqual(Routes.MY_PROJECTS);
});

Cypress.Commands.add("openUploadFiles", () => {
  cy.clickButtonWithName("Settings").switchTab("Data Upload");
});

Cypress.Commands.add("projectSelectorContinue", (select) => {
  if (select === "project") {
    cy.withinTableRows(DataCy.selectionProjectList, (tr) => {
      tr.eq(1).click();
    });
  } else if (select === "version") {
    cy.withinTableRows(DataCy.selectionVersionList, (tr) => {
      tr.eq(1).click();
    });
  } else {
    cy.clickButton(DataCy.stepperContinueButton);
  }
});

Cypress.Commands.add("createNewVersion", (type) => {
  const selectors: Record<typeof type, string> = {
    major: DataCy.versionCreateMajorButton,
    minor: DataCy.versionCreateMinorButton,
    revision: DataCy.versionCreateRevisionButton,
  };

  cy.clickButton(DataCy.selectorAddButton, "last");

  cy.getCy(DataCy.versionCreateModal).within(() => {
    cy.clickButton(selectors[type]);
  });
});
