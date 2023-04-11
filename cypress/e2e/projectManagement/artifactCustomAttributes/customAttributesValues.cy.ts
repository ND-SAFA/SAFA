import { DataCy, customAttribute, customLayout } from "@/fixtures";

describe("Custom Attributes Values", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProject().initProjectVersion();
  });

  describe("I can edit custom attribute values on artifacts", () => {
    it("Creates a custom attribute and layout and edits this on the artifact", () => {
      cy.clickButton(DataCy.navSettingsButton);
      cy.clickButtonWithName("Custom Attributes");
      cy.createCustomAttribute(customAttribute);
      cy.createCustomLayout(customLayout);

      // Navigate to the artifact and edit the custom attribute
      cy.clickButton(DataCy.navArtifactViewButton);
      cy.clickButton(DataCy.navTableButton);
      cy.clickButtonWithName("F8");
      cy.clickButton(DataCy.selectedPanelEditButton);
      cy.contains("label", customAttribute.label);
      cy.getCy(DataCy.selectedPanelCustomAttribute)
        .find("input")
        .type("Test Value");

      cy.clickButton(DataCy.artifactSaveSubmitButton);
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("I can see custom attributes values on artifacts", () => {
    it("Creates a custom attribute and layout and verifies that the value is present on the artifact", () => {
      cy.clickButton(DataCy.navSettingsButton);
      cy.clickButtonWithName("Custom Attributes");
      cy.createCustomAttribute(customAttribute);
      cy.createCustomLayout(customLayout);

      // Navigate to the artifact and edit the custom attribute
      cy.clickButton(DataCy.navArtifactViewButton);
      cy.clickButton(DataCy.navTableButton);
      cy.clickButtonWithName("F8");
      cy.clickButton(DataCy.selectedPanelEditButton);
      cy.contains("label", customAttribute.label);
      cy.getCy(DataCy.selectedPanelCustomAttribute)
        .find("input")
        .type("Test Value");
      cy.clickButton(DataCy.artifactSaveSubmitButton);
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      // Now verify that the value is present on the artifact
      cy.reload();
      cy.clickButtonWithName("F8");
      cy.contains("Test Value");
    });
  });

  describe.skip("I can import artifact custom attribute from CSV or JSON", () => {
    it("Imports custom attributes from CSV and verifies that elements are present", () => {});
    it("Imports custom attributes from JSON and verifies that elements are present", () => {});
  });

  describe.skip("I can export artifact custom attribute to CSV or JSON", () => {
    it("Creates custom attributes and exports them to CSV", () => {});
    it("Creates custom attributes and exports them to JSON", () => {});
  });
});
