import { customLayout, DataCy } from "@/fixtures";

Cypress.Commands.add("createCustomAttribute", (customAttribute) => {
  cy.clickButton(DataCy.addAttributeButton);
  cy.inputText(DataCy.attributeKeyInput, customAttribute.key);
  cy.inputText(DataCy.attributeLabelInput, customAttribute.label);
  cy.inputText(DataCy.attributeMinInput, customAttribute.min);
  cy.inputText(DataCy.attributeMaxInput, customAttribute.max);
  cy.clickButton(DataCy.attributeSaveButton);

  // Verify that the attribute was added
  cy.getCy(DataCy.snackbarSuccess).should("be.visible");
  cy.getCy(DataCy.attributeTableItem).should("be.visible");
});

Cypress.Commands.add("createCustomLayout", (customLayout) => {
  cy.clickButton(DataCy.attributeLayoutAddButton);
  cy.clickButton(DataCy.attributeTableItemPlusButton);
  cy.inputText(DataCy.attributeLayoutNameInput, customLayout.name);
  cy.inputText(DataCy.attributeLayoutTypeInput, customLayout.type);
  cy.clickButton(DataCy.attributeLayoutSaveButton);

  // Verify that the layout was added
  cy.getCy(DataCy.snackbarSuccess).should("be.visible");
  cy.clickButtonWithName(customLayout.name)
    .should("be.visible")
    .and("contain", customLayout.name);
});
