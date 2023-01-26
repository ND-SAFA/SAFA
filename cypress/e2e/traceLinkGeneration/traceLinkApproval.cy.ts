import { before } from "mocha";
import { DataCy } from "../../fixtures";
import { validUser } from "../../fixtures/data/user.json";

describe("Trace Link Approval", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects();
  });

  describe("Trace Link Approval Changes", () => {
    beforeEach(() => {
      cy.viewport(1024, 768);

      cy.visit("/create")
        .login(validUser.email, validUser.password)
        .location("pathname", { timeout: 2000 })
        .should("equal", "/create");

      cy.createBulkProject()
        .waitForJobLoad()
        .clickButton(DataCy.jobOpenButton)
        .openApproveGeneratedTraceLinks()
        .clickButton(DataCy.sidebarCloseButton);
    });

    describe("I can approve an un-reviewed or declined trace link", () => {
      it("Can approve a trace link and check that it is approved", () => {
        cy.clickButton(DataCy.traceApproveButton);
        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        // To verify that it is approved, we will check for that trace link
        cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
          "{backspace}{downArrow}{enter}{esc}"
        );
        cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
          // The header, group, and trace link rows
          tr.should("have.length", 3);
        });
      });

      it("Can approve a declined trace link and check that it is approved", () => {
        cy.clickButton(DataCy.traceDeclineButton);
        cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
          "{backspace}{downArrow}{downArrow}{enter}{esc}"
        );
        cy.clickButton(DataCy.traceApproveButton);
        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
          "{backspace}{downArrow}{downArrow}{enter}{esc}"
        );
        cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
          // The header, group, and trace link rows
          tr.should("have.length", 3);
        });
      });
    });

    describe("I can decline an un-reviewed or approved trace link", () => {
      it("Can decline a trace link and check that it is declined", () => {
        cy.clickButton(DataCy.traceDeclineButton);
        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
          "{backspace}{downArrow}{downArrow}{enter}{esc}"
        );
        cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
          // The header, group, and trace link rows
          tr.should("have.length", 3);
        });
      });

      it("Can decline an approved trace link and check that it is declined", () => {
        cy.clickButton(DataCy.traceApproveButton);
        cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
          "{backspace}{downArrow}{enter}{esc}"
        );
        cy.clickButton(DataCy.traceDeclineButton);
        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
          "{backspace}{downArrow}{enter}{esc}"
        );
        cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
          // The header, group, and trace link rows
          tr.should("have.length", 3);
        });
      });
    });

    // describe("I cannot see declined trace links on the graph", () => {});
    // describe("I can see un-reviewed trace links as dotted lines", () => {});

    describe("I can un-review an approved or declined trace link", () => {
      it("Can un-review an approved trace link", () => {
        cy.clickButton(DataCy.traceApproveButton);
        cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
          "{backspace}{downArrow}{enter}{esc}"
        );
        cy.clickButton(DataCy.traceUnreviewButton);

        cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
          // Only the header and group rows, no traces
          tr.should("have.length", 2);
        });
      });

      it("Can un-review a declined trace link", () => {
        cy.clickButton(DataCy.traceDeclineButton);
        cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
          "{backspace}{downArrow}{downArrow}{enter}{esc}"
        );
        cy.clickButton(DataCy.traceUnreviewButton);

        cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
          // Only the header and group rows, no traces
          tr.should("have.length", 2);
        });
      });
    });
  });

  describe("Trace Link Approval Display", () => {
    before(() => {
      cy.dbResetJobs().dbResetProjects().loadNewProject();
    });

    beforeEach(() => {
      cy.viewport(1600, 768);

      cy.loadCurrentProject()
        .openApproveGeneratedTraceLinks()
        .clickButton(DataCy.sidebarCloseButton);
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
      it("Can group by type", () => {
        cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
          "{backspace}{downArrow}{enter}{downArrow}{enter}{downArrow}{enter}{esc}"
        );
        cy.clickButton(DataCy.traceLinkTableGroupByInput).type(
          "{backspace}{upArrow}{enter}{esc}"
        );
        cy.clickButton(DataCy.traceLinkTableSortByInput).type(
          "{backspace}{esc}"
        );
        cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
          tr.contains("Source type:").parent().contains("design");
        });
      });

      it("Can group by approval status", () => {
        cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
          "{backspace}{downArrow}{enter}{downArrow}{enter}{downArrow}{enter}{esc}"
        );

        cy.clickButton(DataCy.traceLinkTableSortByInput).type(
          "{backspace}{esc}"
        );
        cy.clickButton(DataCy.traceLinkTableGroupByInput).type(
          "{downArrow}{downArrow}{enter}{esc}"
        );
        cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
          tr.contains("Approval status:").parent().contains("Unreviewed");
        });
      });
    });

    describe("I can see the counts of grouped trace links", () => {
      it("Can see the counts of grouped trace links", () => {
        cy.clickButton(DataCy.traceLinkTableApprovalTypeButton).type(
          "{backspace}{downArrow}{enter}{downArrow}{enter}{downArrow}{enter}{esc}"
        );

        cy.clickButton(DataCy.traceLinkTableSortByInput).type(
          "{backspace}{esc}"
        );
        cy.clickButton(DataCy.traceLinkTableGroupByInput).type(
          "{downArrow}{downArrow}{enter}{esc}"
        );
        cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
          tr.contains("Approval status:").parent().contains("7");
        });
      });
    });
  });
});
