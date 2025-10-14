import { DataCy, customAttribute } from "@/fixtures";
describe("Custom Attributes", () => {
  beforeEach(() => {
    cy.initProject().initProjectVersion();

    // Visit custom attributes tab.
    cy.clickButton(DataCy.navSettingsButton).switchTab("Custom Attributes");
  });

  describe("I can add a custom attribute to my project", () => {
    it("Adds a custom attribute to the project", () => {
      cy.createCustomAttribute(customAttribute);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.attributeTableItem).should("be.visible");
    });
  });

  describe("I can edit a custom attribute on my project", () => {
    it("Creates a custom attribute and edits it", () => {
      cy.createCustomAttribute(customAttribute);

      cy.clickButtonWithName(customAttribute.label)
        .inputText(DataCy.attributeLabelInput, "New Label", true)
        .clickButton(DataCy.attributeSaveButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.attributeTableItem).should("contain", "New Label");
    });
  });

  describe("I can delete a custom attribute on my project", () => {
    it("Creates a custom attribute and deletes it", () => {
      cy.createCustomAttribute(customAttribute);

      cy.clickButtonWithName(customAttribute.label)
        .clickButton(DataCy.attributeDeleteButton)
        .clickButton(DataCy.confirmModalButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.attributeTableItem).should("not.exist");
    });
  });

  // describe.skip("I can generate FMEA attributes for traced artifact children", () => {});

  describe("I cannot change the key or data type of a custom attribute", () => {
    it("Creates a custom attribute and checks that the key and data type are disabled", () => {
      cy.createCustomAttribute(customAttribute);

      cy.clickButtonWithName(customAttribute.label);

      cy.getCy(DataCy.attributeKeyInput).should("be.disabled");

      // Workaround for Quasar select input being designed weirdly.
      cy.getCy(DataCy.attributeTypeInput)
        .parent()
        .parent()
        .parent()
        .parent()
        .should("have.class", "q-field--disabled");
    });
  });
});
