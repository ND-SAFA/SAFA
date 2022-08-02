
Cypress.Commands.add("setProjectInformationInCreator",(name:string,description:string) => {
    cy.getCy("input-project-name").first().type(name);
    cy.getCy("input-project-description").first().type(description);
})