import { DataCy } from "@/fixtures";

describe("Artifact Table View", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion().switchToTableView();
  });

  describe("I can view artifacts in a table", () => {
    it("Shows artifacts in a table", () => {
      cy.withinTableRows(DataCy.artifactTable, (tr) => {
        // 1 Header row, 2 group rows, 19 artifacts x 2 rows each.
        tr.should("have.length", 1 + 2 + 19 * 2);

        tr.eq(3).should("contain.text", "D1");
      });
    });
  });

  describe.skip("I can sort artifacts by their attributes", () => {
    it("Sorts artifacts by type", () => {
      cy.sortArtifactTable("type").groupArtifactTable("none");

      cy.withinTableRows(DataCy.artifactTable, (tr) => {
        tr.then(($els) => {
          // 1 Header row, 14 design artifacts, 5 requirement artifacts x 2 rows each.
          const designRowCount = 1 + 14 * 2;
          const $designs = $els.slice(1, designRowCount);
          const $reqs = $els.slice(designRowCount, designRowCount + 5 * 2);

          cy.wrap($designs).each(($el, idx) => {
            if (idx % 2 === 0) return;

            cy.wrap($el).should("contain", "Design");
          });
          cy.wrap($reqs).each(($el, idx) => {
            if (idx % 2 === 0) return;
            cy.wrap($el).should("contain", "Requirement");
          });
        });
      });
    });
  });

  describe.skip("I can group artifacts by their attributes", () => {
    it("Groups artifacts by name", () => {
      cy.sortArtifactTable("name").groupArtifactTable("name");

      cy.getCy(DataCy.artifactTableGroup)
        .first()
        .within(() => {
          cy.getCy(DataCy.artifactTableGroupType).should("contain", "Name:");
          cy.getCy(DataCy.artifactTableGroupValue).should("contain", "D1");
        });
    });
  });

  describe("I can select an artifact to view more details", () => {
    it("Selects an artifact that is clicked", () => {
      cy.withinTableRows(DataCy.artifactTable, (tr) => {
        tr.contains("D1").click();
      });

      cy.getCy(DataCy.selectedPanelName).should("contain", "D1");
    });
  });
});
