import { DataCy } from "@/fixtures";

Cypress.Commands.add("openDocumentSelector", () => {
  cy.clickButton(DataCy.documentSelectButton, undefined, true);
});

Cypress.Commands.add("openDocumentCreator", () => {
  cy.openDocumentSelector().clickButton(DataCy.documentCreateButton);
});

Cypress.Commands.add("openDocumentEditor", (name) => {
  cy.openDocumentSelector()
    .get(`[data-cy-name="${name}"]`)
    .within(() => {
      cy.clickButton(DataCy.documentEditButton);
    });
});

Cypress.Commands.add(
  "fillDocumentFields",
  ({
    name,
    type,
    includeTypes,
    artifacts,
    includeChildTypes,
    childArtifacts,
  }) => {
    if (name === undefined) name = `New ${Math.random()}`;

    cy.clickButton(DataCy.documentIncludeChildrenToggle);
    cy.inputText(DataCy.documentNameInput, name);

    if (type) {
      cy.clickButton(
        DataCy.documentTypeInput,
        undefined,
        true
      ).clickButtonWithName(type);
    }
    if (includeTypes) {
      cy.inputText(DataCy.documentIncludeTypesInput, `${includeTypes}{esc}`);
    }
    if (artifacts) {
      cy.inputText(DataCy.documentArtifactsInput, `${artifacts}{esc}`);
    }
    if (includeChildTypes) {
      cy.inputText(DataCy.documentChildTypesInput, `${includeChildTypes}{esc}`);
    }
    if (childArtifacts) {
      cy.inputText(
        DataCy.documentChildArtifactsInput,
        `${childArtifacts}{esc}`
      );
    }
  }
);

Cypress.Commands.add("createDocument", (props, save) => {
  cy.openDocumentCreator().fillDocumentFields(props);

  if (!save) return;

  cy.clickButton(DataCy.documentSaveButton);
});
