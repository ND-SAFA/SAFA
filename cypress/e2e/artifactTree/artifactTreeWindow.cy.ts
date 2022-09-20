import { DataCy, DataIds } from "../../fixtures";

describe("Artifact Tree Window", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
  });

  describe("I can re-center the graph", () => {
    it("Makes all nodes centered and visible", () => {
      cy.getNodes().should("not.have.length", 19);
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
        .get(DataIds.rightClickAddArtifact)
        .should("be.visible");
    });
  });

  describe("I can see the graph interactions load on page change", () => {
    it("Loads the graph and is responsive", () => {
      // Visit another page.
      cy.clickButton(DataCy.navProjectButton)
        .clickButtonWithName("Create Project")
        .location("pathname", { timeout: 5000 })
        .should("equal", "/create");

      // Return to the project page.
      cy.go("back")
        .location("pathname", { timeout: 5000 })
        .should("equal", "/project")
        .getCy(DataCy.appLoading)
        .should("not.be.visible");

      // Assert that right clicking works to know that the graph is responsive.
      cy.centerGraph()
        .getNodes()
        .first()
        .rightclick()
        .get(DataIds.rightClickAddArtifact)
        .should("be.visible");
    });
  });

  describe("I can see the graph interactions load on artifact view change", () => {
    it("Loads the graph and is responsive", () => {
      // Toggle back and forth to the artifact table.
      cy.clickButton(DataCy.navToggleView)
        .clickButton(DataCy.navToggleView)
        .getCy(DataCy.appLoading)
        .should("not.be.visible");

      // Assert that right clicking works to know that the graph is responsive.
      cy.centerGraph()
        .getNodes()
        .first()
        .rightclick()
        .get(DataIds.rightClickAddArtifact)
        .should("be.visible");
    });
  });

  describe("I can filter the visibility of artifacts by type", () => {
    it("Fades out filtered artifacts", () => {
      cy.clickButton(DataCy.navGraphFilterButton);
      cy.getCy(DataCy.navGraphFilterOption)
        .filter(":visible")
        .each((el) => cy.wrap(el).click());

      cy.centerGraph().getNodes().should("have.css", "opacity", "0.1");
    });
  });
});
