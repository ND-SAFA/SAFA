import { DataCy } from "@/fixtures";

Cypress.Commands.add("fillCustomAttributeFields", (props) => {
  cy.clickButton(DataCy.addAttributeButton);
  cy.inputText(DataCy.attributeKeyInput, props.key);
  cy.inputText(DataCy.attributeLabelInput, props.label);
  cy.inputText(DataCy.attributeMinInput, props.min);
  cy.inputText(DataCy.attributeMaxInput, props.max);
});

Cypress.Commands.add("createCustomAttribute", (props) => {
  cy.fillCustomAttributeFields(props).clickButton(DataCy.attributeSaveButton);
});

Cypress.Commands.add("fillCustomLayoutFields", (props) => {
  cy.clickButton(DataCy.attributeLayoutAddButton).clickButton(
    DataCy.attributeTableItemPlusButton
  );

  cy.inputText(DataCy.attributeLayoutNameInput, props.name);
  cy.inputText(DataCy.attributeLayoutTypeInput, props.type);
});

Cypress.Commands.add("createCustomLayout", (props) => {
  cy.fillCustomLayoutFields(props).clickButton(
    DataCy.attributeLayoutSaveButton
  );
});
