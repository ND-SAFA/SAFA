import { DataCy } from "@/fixtures";

Cypress.Commands.add("createCustomAttribute", (customAttribute) => {
  cy.clickButton(DataCy.addAttributeButton);
  cy.getCy(DataCy.attributeKeyInput).type(customAttribute.Key);
  cy.getCy(DataCy.attributeLabelInput).type(customAttribute.Label);
  cy.getCy(DataCy.attributeMinInput).type(customAttribute.Min);
  cy.getCy(DataCy.attributeMaxInput).type(customAttribute.Max);
  cy.clickButton(DataCy.attributeSaveButton);

  // Verify that the attribute was added
  cy.getCy(DataCy.snackbarSuccess).should("be.visible");
  cy.getCy(DataCy.attributeTableItem).should("be.visible");
});
