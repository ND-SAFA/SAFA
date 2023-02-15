import { DataCy, customAttribute } from "@/fixtures";
describe("Custom Attributes", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initEmptyProject();
  });

  describe("I can add a custom attribute to my project", () => {
    // TODO: Add a custom attribute to the project
    it("Adds a custom attribute to the project", () => {
      cy.clickButton(DataCy.navSettingsButton);
      cy.clickButtonWithName("Custom Attributes");
      cy.clickButton(DataCy.addAttributeButton);

      // Fill in the form for the attribute
      cy.inputText(DataCy.attributeKeyInput, customAttribute.key);
      cy.inputText(DataCy.attributeLabelInput, customAttribute.label);

      // This selector is disabled in the css from any key or mouse input
      // cy.getCy(DataCy.attributeTypeInput).click().type("{downArrow}{enter}");

      cy.inputText(DataCy.attributeMinInput, customAttribute.min);
      cy.inputText(DataCy.attributeMaxInput, customAttribute.max);
      cy.clickButton(DataCy.attributeSaveButton);

      // Verify that the attribute was added
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.attributeTableItem).should("be.visible");
    });
  });

  describe("I can edit a custom attribute on my project", () => {
    it("Creates a custom attribute and edits it", () => {
      cy.clickButton(DataCy.navSettingsButton);
      cy.clickButtonWithName("Custom Attributes");
      cy.createCustomAttribute(customAttribute);
      cy.clickButtonWithName("Test Label");
      cy.inputText(DataCy.attributeLabelInput, "New Label", true);
      cy.clickButton(DataCy.attributeSaveButton);
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.attributeTableItem)
        .should("be.visible")
        .and("contain", "New Label");
    });
  });

  describe("I can delete a custom attribute on my project", () => {
    it("Creates a custom attribute and deletes it", () => {
      cy.clickButton(DataCy.navSettingsButton);
      cy.clickButtonWithName("Custom Attributes");
      cy.createCustomAttribute(customAttribute);
      cy.clickButtonWithName(customAttribute.label);
      cy.clickButton(DataCy.attributeDeleteButton);
      cy.clickButton(DataCy.confirmModalButton);
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.attributeTableItem).should("not.exist");
    });
  });

  describe.skip("I can generate FMEA attributes for traced artifact children", () => {
    // TODO: Add this test once FMEA attributes are implemented
  });

  describe("I cannot change the key or data type of a custom attribute", () => {
    it("Creates a custom attribute and checks that the key and data type are disabled", () => {
      cy.clickButton(DataCy.navSettingsButton);
      cy.clickButtonWithName("Custom Attributes");
      cy.createCustomAttribute(customAttribute);
      cy.clickButtonWithName(customAttribute.label);

      // Let's make sure that the key and data input fields are disabled
      cy.getCy(DataCy.attributeKeyInput)
        .should("be.disabled")
        .and("have.value", customAttribute.key);
      cy.getCy(DataCy.attributeTypeInput).should("be.disabled");
    });
  });
});
