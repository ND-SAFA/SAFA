import { DataCy } from "../fixtures";

Cypress.Commands.add("openDocumentSelector", () => {
  cy.clickButton(DataCy.documentSelectButton);
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
      cy.clickButton(DataCy.documentTypeInput).clickButtonWithName(type);
    }
    if (includeTypes) {
      cy.inputText(DataCy.documentIncludeTypesInput, includeTypes)
        .getCy(DataCy.documentIncludeTypesInput)
        .within(() => {
          cy.clickButton(DataCy.documentSaveTypesButton);
        });
    }
    if (artifacts) {
      cy.inputText(DataCy.documentArtifactsInput, artifacts)
        .getCy(DataCy.documentArtifactsInput)
        .within(() => {
          cy.clickButton(DataCy.documentSaveArtifactsButton);
        });
    }
    if (includeChildTypes) {
      cy.inputText(DataCy.documentChildTypesInput, includeChildTypes)
        .getCy(DataCy.documentChildTypesInput)
        .within(() => {
          cy.clickButton(DataCy.documentSaveTypesButton);
        });
    }
    if (childArtifacts) {
      cy.inputText(DataCy.documentChildArtifactsInput, childArtifacts)
        .getCy(DataCy.documentChildArtifactsInput)
        .within(() => {
          cy.clickButton(DataCy.documentSaveArtifactsButton);
        });
    }
  }
);

Cypress.Commands.add("createDocument", (props) => {
  cy.openDocumentCreator().fillDocumentFields(props);
});

Cypress.Commands.add("saveDocument", () => {
  cy.getCy(DataCy.documentModal).within(() => {
    cy.clickButton(DataCy.documentSaveButton);
  });
});
