import { DataCy } from "@/fixtures";

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
