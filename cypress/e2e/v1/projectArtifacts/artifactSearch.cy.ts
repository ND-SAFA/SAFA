import { DataCy } from "../../../fixtures";

describe("Artifact Search", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
  });

  describe("I can search through current artifacts", () => {
    it("Searches for an artifact in the nav bar", () => {
      cy.selectArtifact("F21");

      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain", "F21");
    });
  });

  describe("I can see how many artifact match my search", () => {
    it("Displays the count of matching artifacts in the nav bar", () => {
      cy.inputText(DataCy.artifactSearchNavInput, "F21");
      cy.getCy(DataCy.artifactSearchItem).should("have.length", 1);
      cy.getCy(DataCy.artifactSearchCount).should("contain", 1);

      cy.getCy(DataCy.artifactSearchNavInput)
        .clear()
        .inputText(DataCy.artifactSearchNavInput, "Design");
      cy.getCy(DataCy.artifactSearchItem).should("have.length", 14);
      cy.getCy(DataCy.artifactSearchCount).should("contain", 14);
    });
  });
});
