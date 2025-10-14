import { DataCy, customAttribute, customLayout } from "@/fixtures";

describe("Custom Attributes Layout", () => {
  beforeEach(() => {
    cy.initProject().initProjectVersion();

    // Visit custom attributes tab.
    cy.clickButton(DataCy.navSettingsButton).switchTab("Custom Attributes");

    // Create a custom attribute and layout.
    cy.createCustomAttribute(customAttribute)
      .createCustomLayout(customLayout)
      .wait(1000); // Wait to switch to the new layout tab.
  });

  describe("I can add a new attribute layout", () => {
    it("Adds a new custom attribute and creates a layout for it", () => {
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.clickButtonWithName(customLayout.name)
        .should("be.visible")
        .and("contain", customLayout.name);
    });
  });

  describe("I can edit an attribute layout", () => {
    it("Creates a custom attribute and layout and edits the layout", () => {
      cy.inputText(
        DataCy.attributeLayoutNameInput,
        "Edited Layout",
        true
      ).clickButton(DataCy.attributeLayoutSaveButton);

      // Verify that the layout was edited.
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.clickButtonWithName("Edited Layout")
        .should("be.visible")
        .and("contain", "Edited Layout");
    });
  });

  describe("I can delete an attribute layout", () => {
    it("Creates a custom attribute and layout and deletes the layout", () => {
      cy.clickButton(DataCy.attributeLayoutDeleteButton).clickButton(
        DataCy.attributeLayoutConfirmDeleteButton
      );

      // Verify that the layout was deleted
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("I can see different layouts of custom attributes based on an artifact's type", () => {
    it("Verifies that the layout is applied only to the artifact of the correct type", () => {
      cy.clickButton(DataCy.navArtifactViewButton).clickButton(
        DataCy.navTableButton
      );

      // The default layout applies to designs.
      cy.clickButtonWithName("D1");

      cy.getCy(
        DataCy.selectedPanelAttributePrefix + customAttribute.key
      ).should("exist");

      // The default layout does not apply to requirements.
      cy.clickButtonWithName("F10");

      cy.getCy(
        DataCy.selectedPanelAttributePrefix + customAttribute.key
      ).should("not.exist");
    });
  });
});
