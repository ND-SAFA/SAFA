import "cypress-file-upload";
import { DataCy } from "../fixtures";

Cypress.Commands.add("getCy", (dataCy, elementPosition, timeout) => {
  const elementList = cy.get(`[data-cy="${dataCy}"]`, { timeout });
  if (elementPosition === "first") {
    return elementList.first();
  } else if (elementPosition === "last") {
    return elementList.last();
  } else {
    return elementList;
  }
});

Cypress.Commands.add("inputText", (dataCy, inputValue, elementPosition) => {
  cy.getCy(dataCy, elementPosition).type(inputValue);
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
  cy.getCy(dataCy).within(() => cy.clickButton(DataCy.selectionClose));
});
