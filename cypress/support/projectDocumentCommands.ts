import { DataCy } from "../fixtures";

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

    cy.clickButton(DataCy.documentIncludeChildrenToggle, undefined, true);
    cy.inputText(DataCy.documentNameInput, name);

    if (type) {
      cy.clickButton(
        DataCy.documentTypeInput,
        undefined,
        true
      ).clickButtonWithName(type);
    }
    if (includeTypes) {
      cy.inputText(DataCy.documentIncludeTypesInput, includeTypes)
        .getCy(DataCy.documentIncludeTypesInput)
        .within(() => {
          cy.clickButton(DataCy.documentSaveTypesButton, undefined, true);
        });
    }
    if (artifacts) {
      cy.inputText(DataCy.documentArtifactsInput, artifacts)
        .getCy(DataCy.documentArtifactsInput)
        .within(() => {
          cy.clickButton(DataCy.documentSaveArtifactsButton, undefined, true);
        });
    }
    if (includeChildTypes) {
      cy.inputText(DataCy.documentChildTypesInput, includeChildTypes)
        .getCy(DataCy.documentChildTypesInput)
        .within(() => {
          cy.clickButton(DataCy.documentSaveTypesButton, undefined, true);
        });
    }
    if (childArtifacts) {
      cy.inputText(DataCy.documentChildArtifactsInput, childArtifacts)
        .getCy(DataCy.documentChildArtifactsInput)
        .within(() => {
          cy.clickButton(DataCy.documentSaveArtifactsButton, undefined, true);
        });
    }
  }
);

Cypress.Commands.add("createDocument", (props) => {
  cy.openDocumentCreator().fillDocumentFields(props);
});

Cypress.Commands.add("saveDocument", () => {
  cy.getCy(DataCy.documentModal).within(() => {
    cy.clickButton(DataCy.documentSaveButton, undefined, true);
  });
});
