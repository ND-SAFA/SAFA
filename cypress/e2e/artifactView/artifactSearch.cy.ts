import { DataCy } from "../../fixtures";

describe("Artifact Search", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
  });

  describe("I can see all artifacts ordered by type", () => {
    it("Displays all artifact types and counts", () => {
      cy.clickButton(DataCy.navToggleRightPanel);

      cy.getCy(DataCy.artifactSearchTypeList)
        .should("contain", "design")
        .should("contain", "requirement");
    });
  });

  describe("I can search through current artifacts", () => {
    it("Searches for an artifact in the nav bar", () => {
      cy.selectArtifact("F21", "nav");

      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain", "F21");
    });

    it("Searches for an artifact in the side bar", () => {
      cy.selectArtifact("F21", "panel");

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

    it("Displays the count of matching artifacts in the side bar", () => {
      cy.clickButton(DataCy.navToggleRightPanel);

      cy.inputText(DataCy.artifactSearchSideInput, "F21");
      cy.getCy(DataCy.artifactSearchItem).should("have.length", 1);
      cy.getCy(DataCy.artifactSearchCount).should("contain", 1);

      cy.getCy(DataCy.artifactSearchSideInput)
        .clear()
        .inputText(DataCy.artifactSearchSideInput, "Design");
      cy.getCy(DataCy.artifactSearchItem).should("have.length", 14);
      cy.getCy(DataCy.artifactSearchCount).should("contain", 14);
    });
  });
});
