import { DataCy } from "../fixtures";

Cypress.Commands.add("openProjectSelector", () => {
  cy.visit("/open")
    .location("pathname", { timeout: 2000 })
    .should("equal", "/open");
});

Cypress.Commands.add("openUploadFiles", () => {
  cy.clickButtonWithName("Settings").switchTab("Data Upload");
});

Cypress.Commands.add("projectSelectorContinue", (select) => {
  if (select === "project") {
    cy.withinTableRows(DataCy.selectionProjectList, (tr) => {
      tr.should("not.contain", "Loading").should("not.contain", "No");
      tr.last().click();
    });
  } else if (select === "version") {
    cy.withinTableRows(DataCy.selectionVersionList, (tr) => {
      tr.should("not.contain", "Loading").should("not.contain", "No");
      tr.last().click();
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

  cy.getCy(DataCy.selectionVersionList).within(() => {
    cy.clickButton(DataCy.selectorAddButton);
  });

  cy.getCy(DataCy.versionCreateModal).within(() => {
    cy.clickButton(selectors[type]);
  });
});
