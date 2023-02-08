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
        // Header row, 2 group rows, 19 artifacts.
        tr.should("have.length", 22);

        // Name, 19 artifacts.
        cy.get("th").should("have.length", 20);
      });
    });
  });

  describe("I can filter the trace matrix table rows and columns by artifact type", () => {
    it("Filters for requirements to designs", () => {
      cy.filterTraceMatrixTable("req", "des");

      cy.withinTableRows(DataCy.traceMatrixTable, (tr) => {
        // Header row, 1 group row, 5 requirement artifacts.
        tr.should("have.length", 7);

        // Name, 14 design artifacts.
        cy.get("th").should("have.length", 15);
      });
    });
  });

  describe("I can select an artifact to view more details", () => {
    it("Selects an artifact that is clicked", () => {
      cy.withinTableRows(DataCy.traceMatrixTable, (tr) => {
        tr.last().contains("F6").click();
      });

      cy.getCy(DataCy.selectedPanelName).should("contain", "F6");
    });
  });

  describe("I can select a trace link to view more details", () => {
    it("Selects a trace link that is clicked", () => {
      cy.filterTraceMatrixTable("des", "req").clickButton(
        DataCy.sidebarCloseButton
      );

      cy.withinTableRows(DataCy.traceMatrixTable, (tr) => {
        // Scroll and wait for cells to lazy load.
        cy.get(".v-data-table__wrapper").scrollTo("bottom");

        tr.last().contains("F11").click();
      });

      cy.getCy(DataCy.selectedPanelTraceTarget).should("contain", "F11");
      cy.getCy(DataCy.selectedPanelTraceSource).should("contain", "F9");
    });
  });
});
