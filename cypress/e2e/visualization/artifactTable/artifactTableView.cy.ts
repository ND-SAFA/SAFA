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
        // Header row, 2 group rows, 19 artifacts.
        tr.should("have.length", 22);

        cy.getCy(DataCy.artifactTableRowName)
          .first()
          .should("exist")
          .contains("D1");
      });
    });
  });

  describe("I can sort artifacts by their attributes", () => {
    it("Sorts artifacts by type", () => {
      cy.sortArtifactTable("type").groupArtifactTable("none");

      cy.withinTableRows(DataCy.artifactTable, (tr) => {
        tr.then(($els) => {
          // 1 Header row, 14 design artifacts, 5 requirement artifacts.
          const $designs = $els.slice(1, 15);
          const $reqs = $els.slice(15, 20);

          cy.wrap($designs).each(($el) =>
            cy.wrap($el).should("contain", "design")
          );
          cy.wrap($reqs).each(($el) =>
            cy.wrap($el).should("contain", "requirement")
          );
        });
      });
    });
  });

  describe("I can group artifacts by their attributes", () => {
    it("Groups artifacts by name", () => {
      cy.sortArtifactTable("none").groupArtifactTable("name");

      cy.getCy(DataCy.artifactTableGroup)
        .last()
        .within(() => {
          cy.getCy(DataCy.artifactTableGroupType).should("contain", "Name:");
          cy.getCy(DataCy.artifactTableGroupValue).should("contain", "F9");
        });
    });
  });

  describe("I can select an artifact to view more details", () => {
    it("Selects an artifact that is clicked", () => {
      cy.withinTableRows(DataCy.artifactTable, (tr) => {
        tr.last().click();
      });

      cy.getCy(DataCy.selectedPanelName).should("contain", "F6");
    });
  });
});
