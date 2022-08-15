import "cypress-file-upload";

type ElementPosition = "first" | "last";

Cypress.Commands.add(
  "getCy",
  (dataCy: string, elementPosition?: ElementPosition, timeout?: number) => {
    const elementList = cy.get(`[data-cy="${dataCy}"]`, { timeout });
    if (elementPosition === "first") {
      return elementList.first();
    } else if (elementPosition === "last") {
      return elementList.last();
    } else {
      return elementList;
    }
  }
);

Cypress.Commands.add(
  "inputText",
  (
    dataCy: string,
    inputValue: string,
    elementPosition: ElementPosition = "first"
  ) => {
    cy.getCy(dataCy, elementPosition).type(inputValue);
  }
);

Cypress.Commands.add(
  "clickButton",
  (dataCy: string, elementPosition: ElementPosition = "first") => {
    cy.getCy(dataCy, elementPosition).click();
  }
);

Cypress.Commands.add("clickButtonWithName", (name: string) => {
  cy.contains(name, { matchCase: false }).last().click();
});

Cypress.Commands.add("clickMenuOption", (optionName: string) => {
  cy.get(`[role="menu"]`)
    .contains(optionName, { matchCase: false })
    .first()
    .click();
});

Cypress.Commands.add(
  "uploadFiles",
  (dataCy: string, ...filePaths: string[]) => {
    cy.getCy(dataCy, "last").attachFile(filePaths);
  }
);

Cypress.Commands.add("switchTab", (tabLabel: string) => {
  cy.contains("div", tabLabel).click();
});
