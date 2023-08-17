import { DataCy, customAttribute, customLayout } from "@/fixtures";

describe("Custom Attributes Values", () => {
  beforeEach(() => {
    cy.initProject().initProjectVersion();

    // Visit custom attributes tab.
    cy.clickButton(DataCy.navSettingsButton).switchTab("Custom Attributes");

    // Create an attribute and layout.
    cy.createCustomAttribute(customAttribute).createCustomLayout({
      ...customLayout,
      type: "{enter}",
    });

    // View a node on the graph.
    cy.clickButton(DataCy.navArtifactViewButton)
      .clickButton(DataCy.navTableButton)
      .clickButtonWithName("F10");
  });

  describe("I can see custom attributes values on artifacts", () => {
    it("Views a custom attribute on an artifact", () => {
      cy.getCy(
        DataCy.selectedPanelAttributePrefix + customAttribute.key
      ).should("exist");
    });
  });

  describe("I can edit custom attribute values on artifacts", () => {
    it("Edits a custom attribute from an artifact", () => {
      const testValue = "Test Value";

      cy.clickButton(DataCy.selectedPanelEditButton);

      cy.inputText(
        DataCy.selectedPanelAttributeInputPrefix + customAttribute.key,
        testValue,
        false,
        true
      );

      cy.clickButton(DataCy.artifactSaveSubmitButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(
        DataCy.selectedPanelAttributePrefix + customAttribute.key
      ).should("contain.text", testValue);
    });
  });

  // describe.skip("I can import artifact custom attribute from CSV or JSON", () => {
  //   it("Imports custom attributes from CSV and verifies that elements are present", () => {});
  //   it("Imports custom attributes from JSON and verifies that elements are present", () => {});
  // });
  //
  // describe.skip("I can export artifact custom attribute to CSV or JSON", () => {
  //   it("Creates custom attributes and exports them to CSV", () => {});
  //   it("Creates custom attributes and exports them to JSON", () => {});
  // });
});
