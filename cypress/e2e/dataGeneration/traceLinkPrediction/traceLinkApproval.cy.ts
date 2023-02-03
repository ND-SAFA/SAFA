import { DataCy } from "@/fixtures";

describe("Trace Link Approval", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion().openTraceApproval();
  });

  describe("I can approve an un-reviewed or declined trace link", () => {
    it("Can approve a trace link and check that it is approved", () => {
      cy.clickButton(DataCy.traceApproveButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.filterTraceApproval("approved");

      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        // The header, group, and trace link.
        tr.should("have.length", 3);
      });
    });

    it("Can approve a declined trace link and check that it is approved", () => {
      cy.clickButton(DataCy.traceDeclineButton)
        .filterTraceApproval("declined")
        .clickButton(DataCy.traceApproveButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      // Filter for approved links.
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{downArrow}{enter}{esc}"
      );

      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        // The header, group, and trace link.
        tr.should("have.length", 3);
      });
    });
  });

  describe("I can decline an un-reviewed or approved trace link", () => {
    it("Can decline a trace link and check that it is declined", () => {
      cy.clickButton(DataCy.traceDeclineButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.filterTraceApproval("declined");

      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        // The header, group, and trace link.
        tr.should("have.length", 3);
      });
    });

    it("Can decline an approved trace link and check that it is declined", () => {
      cy.clickButton(DataCy.traceApproveButton)
        .filterTraceApproval("approved")
        .clickButton(DataCy.traceDeclineButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      // Filter for approved links.
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{enter}{esc}"
      );

      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        // The header, group, and trace link.
        tr.should("have.length", 3);
      });
    });
  });

  describe("I can un-review an approved or declined trace link", () => {
    it("Can un-review an approved trace link", () => {
      cy.clickButton(DataCy.traceApproveButton)
        .filterTraceApproval("approved")
        .clickButton(DataCy.traceUnreviewButton);

      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        // Only the header and group rows, no traces.
        tr.should("have.length", 2);
      });
    });

    it("Can un-review a declined trace link", () => {
      cy.clickButton(DataCy.traceDeclineButton)
        .filterTraceApproval("declined")
        .clickButton(DataCy.traceUnreviewButton);

      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        // Only the header and group rows, no traces.
        tr.should("have.length", 2);
      });
    });
  });
});
