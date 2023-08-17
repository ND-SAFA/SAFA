import { DataCy } from "@/fixtures";

describe.skip("Trace Link Approval Display", () => {
  before(() => {
    cy.initProject(true, true);
  });

  beforeEach(() => {
    cy.initProjectVersion().switchToTableView("approval");
  });

  describe("I can see approved, declined, and un-reviewed trace links", () => {
    it("Displays all generated links", () => {
      cy.filterTraceApproval("all")
        .sortTraceApproval("none")
        .groupTraceApproval("none");

      cy.withinTableRows(
        DataCy.traceLinkTable,
        (tr) => {
          // 1 Header row, 2 virtual scrolls, 7 links x 2 rows per each
          tr.should("have.length", 1 + 2 + 7 * 2);
        },
        false
      );
    });
  });

  describe("I can sort trace links by their fields", () => {
    it("Can sort by name", () => {
      cy.filterTraceApproval("all")
        .sortTraceApproval("name")
        .groupTraceApproval("none");

      // Should have D9 first and D5 second in order of name (descending)
      cy.withinTableRows(
        DataCy.traceLinkTable,
        (tr) => {
          tr.contains("D9").should("have.length", 1);
          tr.contains("D9")
            .parent()
            .parent()
            .next()
            .next()
            .contains("D5")
            .should("have.length", 1);
        },
        false
      );
    });
  });

  describe("I can group trace links by their fields", () => {
    it("Can group by type", () => {
      cy.filterTraceApproval("all")
        .sortTraceApproval("none")
        .groupTraceApproval("type");

      cy.withinTableRows(
        DataCy.traceLinkTable,
        (tr) => {
          tr.contains("Source type:").parent().contains("Design");
        },
        false
      );
    });

    it("Can group by approval status", () => {
      cy.filterTraceApproval("all")
        .sortTraceApproval("none")
        .groupTraceApproval("status");

      cy.withinTableRows(
        DataCy.traceLinkTable,
        (tr) => {
          tr.contains("Approval status:").parent().contains("Unreviewed");
        },
        false
      );
    });
  });

  describe("I can see the counts of grouped trace links", () => {
    it("Can see the counts of grouped trace links", () => {
      cy.filterTraceApproval("all")
        .sortTraceApproval("none")
        .groupTraceApproval("status");

      cy.withinTableRows(
        DataCy.traceLinkTable,
        (tr) => {
          tr.contains("Approval status:").parent().contains("7");
        },
        false
      );
    });
  });
});
