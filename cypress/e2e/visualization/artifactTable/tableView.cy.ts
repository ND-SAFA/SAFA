import { DataCy } from "@/fixtures";

describe("Table View", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion().switchToTableView();
  });

  describe("I can view artifacts in a table", () => {
    it("Shows the first artifact in the table", () => {
      cy.getCy(DataCy.artifactTableArtifact)
        .first()
        .should("exist")
        .contains("D1");
    });
  });

  describe("I can sort artifacts by their attributes", () => {
    it("Sorts artifacts by type", () => {
      // Sort by type.
      cy.clickButton(DataCy.artifactTableSortBy).type(
        "{enter}{downArrow}{enter}"
      );
      // Remove grouping.
      cy.clickButton(DataCy.artifactTableGroupBy).type(
        "{backspace}{backspace}{backspace}{backspace}{esc}"
      );

      cy.get(DataCy.artifactTableNameHeaderNotSorted).should("exist");
      cy.get(DataCy.artifactTableTypeHeaderSortedAsc).should("exist");
    });
  });

  describe("I can group artifacts by their attributes", () => {
    it("Groups artifacts by name", () => {
      // Remove sorting.
      cy.clickButton(DataCy.artifactTableSortBy).type(
        "{backspace}{backspace}{backspace}{backspace}{esc}"
      );
      // Group by name.
      cy.clickButton(DataCy.artifactTableGroupBy).type("{upArrow}{enter}");

      cy.getCy(DataCy.artifactTableGroupByTableHeader)
        .should("exist")
        .contains("Name:");
    });
  });
});
