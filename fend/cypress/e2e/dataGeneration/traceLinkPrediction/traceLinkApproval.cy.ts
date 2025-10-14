import { DataCy } from "@/fixtures";

// 1 header row, 2 virtual scrolls, no traces.
const emptyMatchRowCount = 1 + 2;

// 1 header row, 2 virtual scrolls, 1 group row, 1 trace x 2 rows each.
const singleMatchRowCount = 1 + 2 + 1 + 2;

describe.skip("Trace Link Approval", () => {
  before(() => {
    cy.initProject(true, true);
  });

  beforeEach(() => {
    cy.initProjectVersion().switchToTableView("approval");
  });

  describe("I can approve an un-reviewed or declined trace link", () => {
    it("Can approve a trace link and check that it is approved", () => {
      cy.clickButton(DataCy.traceApproveButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.filterTraceApproval("approved");

      cy.withinTableRows(
        DataCy.traceLinkTable,
        (tr) => {
          tr.should("have.length", singleMatchRowCount);
        },
        false
      );
    });

    it("Can approve a declined trace link and check that it is approved", () => {
      cy.clickButton(DataCy.traceDeclineButton)
        .filterTraceApproval("declined")
        .clickButton(DataCy.traceApproveButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.filterTraceApproval("approved");

      cy.withinTableRows(
        DataCy.traceLinkTable,
        (tr) => {
          tr.should("have.length", singleMatchRowCount);
        },
        false
      );
    });
  });

  describe("I can decline an un-reviewed or approved trace link", () => {
    it("Can decline a trace link and check that it is declined", () => {
      cy.clickButton(DataCy.traceDeclineButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.filterTraceApproval("declined");

      cy.withinTableRows(
        DataCy.traceLinkTable,
        (tr) => {
          tr.should("have.length", singleMatchRowCount);
        },
        false
      );
    });

    it("Can decline an approved trace link and check that it is declined", () => {
      cy.clickButton(DataCy.traceApproveButton)
        .filterTraceApproval("approved")
        .clickButton(DataCy.traceDeclineButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.filterTraceApproval("declined");

      cy.withinTableRows(
        DataCy.traceLinkTable,
        (tr) => {
          tr.should("have.length", singleMatchRowCount);
        },
        false
      );
    });
  });

  describe("I can un-review an approved or declined trace link", () => {
    it("Can un-review an approved trace link", () => {
      cy.clickButton(DataCy.traceApproveButton)
        .filterTraceApproval("approved")
        .clickButton(DataCy.traceUnreviewButton);

      cy.withinTableRows(
        DataCy.traceLinkTable,
        (tr) => {
          tr.should("have.length", emptyMatchRowCount);
        },
        false
      );
    });

    it("Can un-review a declined trace link", () => {
      cy.clickButton(DataCy.traceDeclineButton)
        .filterTraceApproval("declined")
        .clickButton(DataCy.traceUnreviewButton);

      cy.withinTableRows(
        DataCy.traceLinkTable,
        (tr) => {
          tr.should("have.length", emptyMatchRowCount);
        },
        false
      );
    });
  });
});
