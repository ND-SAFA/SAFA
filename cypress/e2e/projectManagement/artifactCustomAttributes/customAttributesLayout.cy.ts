import { DataCy, customAttribute, customLayout } from "@/fixtures";

describe("Custom Attributes Layout", () => {
  beforeEach(() => {
    cy.initProject().initProjectVersion();
  });

  describe("I can add a new attribute layout", () => {
    it("Adds a new custom attribute and creates a layout for it", () => {
      cy.clickButton(DataCy.navSettingsButton);
      cy.clickButtonWithName("Custom Attributes");
      cy.createCustomAttribute(customAttribute);
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
  });

  describe("I can edit an attribute layout", () => {
    it("Creates a custom attribute and layout and edits the layout", () => {
      cy.clickButton(DataCy.navSettingsButton);
      cy.clickButtonWithName("Custom Attributes");
      cy.createCustomAttribute(customAttribute);
      cy.createCustomLayout(customLayout);

      // Now edit this layout
      cy.inputText(DataCy.attributeLayoutNameInput, "Edited Layout", true);
      cy.clickButton(DataCy.attributeLayoutSaveButton);

      // Verify that the layout was edited
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.clickButtonWithName("Edited Layout")
        .should("be.visible")
        .and("contain", "Edited Layout");
    });
  });

  describe("I can delete an attribute layout", () => {
    it("Creates a custom attribute and layout and deletes the layout", () => {
      cy.clickButton(DataCy.navSettingsButton);
      cy.clickButtonWithName("Custom Attributes");
      cy.createCustomAttribute(customAttribute);
      cy.createCustomLayout(customLayout);

      // Now delete this layout
      cy.clickButton(DataCy.attributeLayoutDeleteButton);
      cy.clickButton(DataCy.attributeLayoutConfirmDeleteButton);

      // Verify that the layout was deleted
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("I can see different layouts of custom attributes based on an artifact's type", () => {
    it("Creates a custom attribute and layout and verifies that the layout is applied to the artifact of the correct type", () => {
      cy.clickButton(DataCy.navSettingsButton);
      cy.clickButtonWithName("Custom Attributes");
      cy.createCustomAttribute(customAttribute);
      cy.createCustomLayout(customLayout); // By default, designs are selected

      // Now check if this is present in the artifact
      cy.clickButton(DataCy.navArtifactViewButton);
      cy.clickButton(DataCy.navTableButton);
      cy.clickButtonWithName("D1");
      cy.clickButton(DataCy.selectedPanelEditButton);
      cy.contains("label", customAttribute.label);
    });
  });
});
