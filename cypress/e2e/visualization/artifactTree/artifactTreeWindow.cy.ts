import { DataCy, Routes } from "@/fixtures";

describe("Artifact Tree Window", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion();
  });

  describe("I can re-center the graph", () => {
    it("Makes all nodes centered and visible", () => {
      cy.centerGraph();
      cy.getNodes().should("have.length", 19);
    });
  });

  describe("I can see the graph interactions load on initial page load", () => {
    it("Loads the graph and is responsive", () => {
      // Assert that right clicking works to know that the graph is responsive.
      cy.centerGraph()
        .getNodes()
        .first()
        .rightclick()
        .getCy(DataCy.rightClickAddArtifact)
        .should("be.visible");
    });
  });

  describe("I can see the graph interactions load on page change", () => {
    it("Loads the graph and is responsive", () => {
      // Visit another page.
      cy.clickButtonWithName("Create Project").locationShouldEqual(
        Routes.PROJECT_CREATOR
      );

      // Return to the project page.
      cy.go("back")
        .locationShouldEqual(Routes.ARTIFACT)
        .waitForProjectLoad(true);

      // Assert that right clicking works to know that the graph is responsive.
      cy.centerGraph()
        .getNodes()
        .first()
        .rightclick()
        .getCy(DataCy.rightClickAddArtifact)
        .should("be.visible");
    });
  });

  describe("I can see the graph interactions load on artifact view change", () => {
    it("Loads the graph and is responsive", () => {
      // Toggle back and forth to the artifact table.
      cy.clickButton(DataCy.navTableButton)
        .clickButton(DataCy.navTreeButton)
        .getCy(DataCy.appLoading)
        .should("not.exist");

      // Assert that right clicking works to know that the graph is responsive.
      cy.centerGraph()
        .getNodes()
        .first()
        .rightclick()
        .getCy(DataCy.rightClickAddArtifact)
        .should("be.visible");
    });
  });

  describe.skip("I can filter the visibility of artifacts by type", () => {
    it("Fades out filtered artifacts", () => {
      cy.clickButton(DataCy.navGraphFilterButton);

      cy.getCy(DataCy.navGraphFilterOption)
        .filter(":visible")
        .each((el) => cy.wrap(el).click());

      cy.centerGraph().getNodes().should("have.css", "opacity", "0.3");
    });
  });
});
