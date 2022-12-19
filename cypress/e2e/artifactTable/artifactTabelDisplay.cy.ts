import { DataCy } from "../../fixtures";

describe("Artifact Table Display", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
    cy.switchToTableView();
  });

  describe("I can view artifacts in a table", () => {
    it("Shows the first artifact in the table", () => {
      cy.artifactTableFirstElementLookUp().should("exist").contains("D1");
    });
  });

  describe("I can sort artifacts by their attributes", () => {
    it("Sorts artifacts by type", () => {
      cy.clickButton(DataCy.artifactTableSortBy).type(
        "{enter}{downArrow}{enter}"
      );
      cy.clickButton(DataCy.artifactTableGroupBy).type(
        "{backspace}{backspace}{backspace}{backspace}{esc}"
      );
      cy.get(DataCy.artifactTableNameHeaderNotSorted).should("exist");

      cy.get(DataCy.artifactTableTypeHeaderSortedAsc).should("exist");
    });
  });

  describe("I can group artifacts by their attributes", () => {
    it("Groups artifacts by name", () => {
      cy.clickButton(DataCy.artifactTableSortBy).type(
        "{backspace}{backspace}{backspace}{backspace}{esc}"
      );
      cy.clickButton(DataCy.artifactTableGroupBy).type("{upArrow}{enter}");

      cy.getCy(DataCy.artifactTableGroupByTableHeader)
        .should("exist")
        .contains("Name:");
    });
  });

  describe("I can see project warnings in the artifact table", () => {
    it("Shows a project warning on the artifact table for this project", () => {
      cy.clickButton(DataCy.artifactTableSortBy).type(
        "{backspace}{backspace}{backspace}{backspace}{esc}"
      );
      cy.clickButton(DataCy.artifactTableGroupBy).type(
        "{backspace}{backspace}{backspace}{backspace}{esc}"
      );
      cy.getCy(DataCy.artifactTableArtifactWarning).should("exist");
      cy.clickButton(DataCy.artifactTableArtifactWarning);
      cy.getCy(DataCy.artifactTableArtifactWarningLabel).should("exist");
    });
  });
});
