import { DataCy } from "@/fixtures";

describe("Trace Link Approval Display", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion().openTraceApproval();
  });

  describe("I can see approved, declined, and un-reviewed trace links", () => {
    it("Displays all generated links", () => {
      cy.filterTraceApproval("all")
        .sortTraceApproval("none")
        .groupTraceApproval("none");

      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.should("have.length", 8);
      });
    });
  });

  describe("I can sort trace links by their fields", () => {
    it("Can sort by name", () => {
      cy.filterTraceApproval("all")
        .sortTraceApproval("name")
        .groupTraceApproval("none");

      // Should have D9 first and D5 second in order of name (descending)
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.contains("D9").should("have.length", 1);
        tr.contains("D9")
          .parent()
          .next()
          .contains("D5")
          .should("have.length", 1);
      });
    });

    it("Can sort by approval status", () => {
      cy.filterTraceApproval("all")
        .sortTraceApproval("approval")
        .groupTraceApproval("none");

      // Check that unreviewed pops up and that approval status is bold.
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.contains("Approval Status").should(($label) => {
          expect($label).to.have.css("font-weight", "700");
        });
      });
    });
  });

  describe("I can group trace links by their fields", () => {
    it("Can group by type", () => {
      cy.filterTraceApproval("all")
        .sortTraceApproval("none")
        .groupTraceApproval("type");

      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.contains("Source type:").parent().contains("design");
      });
    });

    it("Can group by approval status", () => {
      cy.filterTraceApproval("all")
        .sortTraceApproval("none")
        .groupTraceApproval("status");

      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.contains("Approval status:").parent().contains("Unreviewed");
      });
    });
  });

  describe("I can see the counts of grouped trace links", () => {
    it("Can see the counts of grouped trace links", () => {
      cy.filterTraceApproval("all")
        .sortTraceApproval("none")
        .groupTraceApproval("status");

      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.contains("Approval status:").parent().contains("7");
      });
    });
  });
});
