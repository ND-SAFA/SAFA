Cypress.Commands.add("inputText", (inputLabel: string, inputValue: string) => {
  cy.contains("label", inputLabel)
    .invoke("attr", "for")
    .then((id) => cy.get(`#${id}`))
    .type(inputValue);
});

Cypress.Commands.add("clickButton", (buttonLabel: string) => {
  cy.contains("span", buttonLabel).parent().click();
});

Cypress.Commands.add("getButton", (buttonLabel: string) => {
  return cy.contains("span", buttonLabel).parent();
});
