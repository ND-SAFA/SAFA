import "cypress-file-upload";

Cypress.Commands.add("getCy", (dataCy: string, timeout?: number) => {
  return cy.get(`[data-cy="${dataCy}"]`, { timeout });
});

Cypress.Commands.add("inputText", (dataCy: string, inputValue: string) => {
  cy.getCy(dataCy).first().type(inputValue);
});

Cypress.Commands.add("clickButton", (dataCy: string) => {
  cy.getCy(dataCy).first().click();
});

Cypress.Commands.add(
  "uploadFiles",
  (dataCy: string, ...filePaths: string[]) => {
    cy.getCy(dataCy).first().attachFile(filePaths);
  }
);

Cypress.Commands.add("switchTab", (tabLabel: string) => {
  cy.contains("div", tabLabel).click();
});
