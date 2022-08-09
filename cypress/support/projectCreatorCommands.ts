Cypress.Commands.add(
  "setProjectInformationInStandardUpload",
  (name: string, description: string) => {
    cy.getCy("input-project-name").first().type(name);
    cy.getCy("input-project-description").first().type(description);
  }
);

Cypress.Commands.add("selectForPossibleErros", (containsErros: boolean) => {}); //need to finish command
