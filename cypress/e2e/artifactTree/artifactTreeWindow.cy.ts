import { DataCy } from "../../fixtures";

describe("Artifact Tree Window", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
  });

  describe("I can filter the visibility of artifacts by type", () => {
    it("Fades out filtered artifacts", () => {
      cy.clickButton(DataCy.navGraphFilterButton);
      cy.getCy(DataCy.navGraphFilterOption)
        .filter(":visible")
        .each((el) => cy.wrap(el).click());

      cy.getNodes().should("have.css", "opacity", "0.1");
    });
  });

  describe("I can re-center the graph", () => {
    it("Makes all nodes centered and visible", () => {
      cy.getNodes().should("not.have.length", 19);
      cy.centerGraph();
      cy.getNodes().should("have.length", 19);
    });
  });
});
