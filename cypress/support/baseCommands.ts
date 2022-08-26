import "cypress-file-upload";
import { DataCy } from "../fixtures";

Cypress.Commands.add("getCy", (dataCy, elementPosition, timeout) => {
  const elements = cy.get(`[data-cy="${dataCy}"]`, { timeout });

  if (elementPosition === "first") {
    return elements.first();
  } else if (elementPosition === "last") {
    return elements.last();
  } else {
    return elements;
  }
});

Cypress.Commands.add("doesExist", (dataCy) => {
  return cy.get("body").then((body) => {
    return body.find(`[data-cy="${dataCy}"]`).length > 0;
  });
});

Cypress.Commands.add("inputText", (dataCy, inputValue, clear) => {
  if (clear) {
    cy.getCy(dataCy).clear();
  }

  if (inputValue.length > 0) {
    cy.getCy(dataCy).type(inputValue);
  }
});

Cypress.Commands.add("clickButton", (dataCy, elementPosition = "first") => {
  cy.getCy(dataCy, elementPosition).click();
});

Cypress.Commands.add("clickButtonWithName", (name) => {
  cy.contains(name, { matchCase: false }).last().click();
});

Cypress.Commands.add("clickMenuOption", (optionName) => {
  cy.get(`[role="menu"]`)
    .contains(optionName, { matchCase: false })
    .first()
    .click();
});

Cypress.Commands.add("uploadFiles", (dataCy, ...filePaths) => {
  cy.getCy(dataCy, "last").attachFile(filePaths);
});

Cypress.Commands.add("switchTab", (tabLabel) => {
  cy.contains("div", tabLabel).click();
});

Cypress.Commands.add("closeModal", (dataCy) => {
  cy.getCy(dataCy).within(() => cy.clickButton(DataCy.modalClose));
});

Cypress.Commands.add("withinTableRows", (dataCy, fn) => {
  cy.getCy(dataCy).within(() => {
    fn(cy.get("tr"));
  });
});
