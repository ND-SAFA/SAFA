import { DataCy } from "@/fixtures";

describe("Trace Matrix Table View", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion().switchToTableView("trace");
  });

  describe("I can view artifacts in a trace matrix table", () => {
    it("Shows artifacts in a trace matrix", () => {
      cy.withinTableRows(DataCy.traceMatrixTable, (tr) => {
        // Header row, 2 group rows, 19 artifacts x 2 rows each.
        tr.should("have.length", 1 + 2 + 19 * 2);

        // Name, Type, 19 artifacts.
        cy.get("th").should("have.length", 1 + 1 + 19);
      });
    });
  });

  describe("I can filter the trace matrix table rows and columns by artifact type", () => {
    it("Filters for requirements to designs", () => {
      cy.filterTraceMatrixTable("req", "des");

      cy.withinTableRows(DataCy.traceMatrixTable, (tr) => {
        // Header row, 2 virtual scroll, 5 requirement artifacts x 2 rows each, 1 footer.
        tr.should("have.length", 1 + 2 + 5 * 2);

        // Name, Type, 14 design artifacts.
        cy.get("th").should("have.length", 1 + 1 + 14);
      });
    });
  });

  describe("I can select an artifact to view more details", () => {
    it("Selects an artifact that is clicked", () => {
      const artifactName = "D1";

      cy.withinTableRows(DataCy.traceMatrixTable, () => {
        cy.get(".q-tr").contains(artifactName).click();
      });

      cy.getCy(DataCy.selectedPanelName).should("contain", artifactName);
    });
  });

  describe("I can select a trace link to view more details", () => {
    it("Selects a trace link that is clicked", () => {
      const sourceName = "D1";
      const targetName = "F5";

      cy.filterTraceMatrixTable("des", "req");

      cy.withinTableRows(DataCy.traceMatrixTable, () => {
        cy.get(".q-tr").contains(targetName).click();
      });

      cy.getCy(DataCy.selectedPanelTraceTarget).should("contain", targetName);
      cy.getCy(DataCy.selectedPanelTraceSource).should("contain", sourceName);
    });
  });
});
