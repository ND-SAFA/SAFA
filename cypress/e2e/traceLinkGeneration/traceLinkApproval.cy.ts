import { DataCy } from "../../fixtures";

describe("Trace Link Approval", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject().openApproveGeneratedTraceLinks();
  });

  describe("I can approve an un-reviewed or declined trace link", () => {
    it("Can decline a trace link and check that it is declined", () => {
      cy.clickButton(DataCy.traceLinkTableGenerateTraceLinkDeclineButton);
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      // To verify that it is declined, we will check for that trace link
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{downArrow}{enter}{esc}"
      );
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        // Has length 3 for heading, group, and trace link itself
        tr.should("have.length", 3);
        tr.contains("D10").should("have.length", 1);
      });
    });

    it("Can approve an un-reviewed trace link and check that it is approved", () => {
      cy.clickButton(DataCy.traceLinkTableGenerateTraceLinkApproveButton);
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      // To verify that it is approved, we will check for that trace link
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{enter}{esc}"
      );
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.should("have.length", 3);
        tr.contains("D2").should("have.length", 1);
      });
    });

    it("Can approve a declined trace link and check that it is approved", () => {
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{downArrow}{enter}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableGenerateTraceLinkApproveButton);
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{downArrow}{enter}{esc}"
      );
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.should("have.length", 4);
        tr.contains("D10").should("have.length", 1);
      });
    });
  });

  describe("I can decline an un-reviewed or approved trace link", () => {
    it("Can decline an un-reviewed trace link and check that it is declined", () => {
      cy.clickButton(DataCy.traceLinkTableGenerateTraceLinkDeclineButton);
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{downArrow}{enter}{esc}"
      );
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.should("have.length", 3);
        tr.contains("D4").should("have.length", 1);
      });
    });

    it("Can decline an approved trace link and check that it is declined", () => {
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{enter}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableGenerateTraceLinkDeclineButton);
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{enter}{esc}"
      );
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.should("have.length", 4);
        tr.contains("D10").should("have.length", 1);
      });
    });
  });

  /* These will be skipped for now
  //TODO: Figure out how to test for trace links on the actual graph
  describe("I cannot see declined trace links on the graph", () => {});
  describe("I can see un-reviewed trace links as dotted lines", () => {});
  */
  describe("I can un-review an approved or declined trace link", () => {
    it("Can un-review an approved trace link", () => {
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{enter}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableGenerateTraceLinkUnapproveButton);
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{downArrow}{enter}{esc}"
      );
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.contains("D2").should("have.length", 1);
      });
    });

    it("Can un-review a declined trace link", () => {
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{downArrow}{enter}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableGenerateTraceLinkUnapproveButton);
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{enter}{esc}"
      );
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.contains("D10").should("have.length", 1);
      });
    });
  });

  describe("I can sort trace links by name, type, and approval status", () => {
    it("Can sort by name", () => {
      // Let make sure all review categories are selected
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{enter}{downArrow}{enter}{downArrow}{enter}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableGroupByInput).type(
        "{backspace}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableSortByInput).type(
        "{enter}{downArrow}{enter}{esc}"
      );
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

    it("Can sort by type", () => {
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{enter}{downArrow}{enter}{downArrow}{enter}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableGroupByInput).type(
        "{backspace}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableSortByInput).type(
        "{backspace}{downArrow}{downArrow}{enter}{esc}"
      );
      // Should have D9 first and D5 second in order of type (descending)
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.contains("D5")
          .should("have.length", 1)
          .parent()
          .should("contain", "design");
        tr.contains("D5").parent().next().should("contain", "design");
      });
    });

    it("Can sort by approval status", () => {
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{enter}{downArrow}{enter}{downArrow}{enter}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableGroupByInput).type(
        "{backspace}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableSortByInput).type(
        "{backspace}{upArrow}{enter}{esc}"
      );
      // Check that unreviewed pops up and that approval status is bold
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.contains("Approval Status").should(($label) => {
          expect($label).to.have.css("font-weight", "700");
        });
      });
    });
  });

  describe("I can group trace links by name, type, and approval status", () => {
    it("Can group by name", () => {
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{enter}{downArrow}{enter}{downArrow}{enter}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableGroupByInput).type(
        "{backspace}{upArrow}{upArrow}{enter}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableSortByInput).type("{backspace}{esc}");
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.contains("Source name:").parent().contains("D10");
      });
    });

    it("Can group by type", () => {
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{enter}{downArrow}{enter}{downArrow}{enter}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableGroupByInput).type(
        "{backspace}{upArrow}{enter}{esc}"
      );
      cy.clickButton(DataCy.traceLinkTableSortByInput).type("{backspace}{esc}");
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.contains("Source type:").parent().contains("design");
      });
    });

    it("Can group by approval status", () => {
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{enter}{downArrow}{enter}{downArrow}{enter}{esc}"
      );

      cy.clickButton(DataCy.traceLinkTableSortByInput).type("{backspace}{esc}");
      cy.clickButton(DataCy.traceLinkTableGroupByInput).type(
        "{downArrow}{downArrow}{enter}{esc}"
      );
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.contains("Approval status:").parent().contains("Declined");
      });
    });
  });

  describe("I can see the counts of grouped trace links", () => {
    it("Can see the counts of grouped trace links", () => {
      cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
        "{backspace}{downArrow}{enter}{downArrow}{enter}{downArrow}{enter}{esc}"
      );

      cy.clickButton(DataCy.traceLinkTableSortByInput).type("{backspace}{esc}");
      cy.clickButton(DataCy.traceLinkTableGroupByInput).type(
        "{downArrow}{downArrow}{enter}{esc}"
      );
      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.contains("Approval status:").parent().contains("1");
      });
    });
  });
});
