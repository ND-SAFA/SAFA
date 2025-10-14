import { DataCy } from "@/fixtures";

describe("Artifact Search", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion();
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
      cy.enableBasicSearch().inputText(DataCy.artifactSearchNavInput, "F21");

      cy.getCy(DataCy.artifactSearchItem).should("have.length", 1);
      cy.getCy(DataCy.artifactSearchCount).should("contain", 1);

      cy.inputText(DataCy.artifactSearchNavInput, "Design", true);

      cy.getCy(DataCy.artifactSearchItem).should("have.length", 14);
      cy.getCy(DataCy.artifactSearchCount).should("contain", 14);
    });
  });
});
