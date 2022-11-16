import { describe } from "mocha";
import { validUser, DataCy } from "../../fixtures";

describe("Job Submission", () => {
  beforeEach(() => {
    cy.dbResetJobs().dbResetProjects();

    cy.visit("/create")
      .login(validUser.email, validUser.password)
      .location("pathname", { timeout: 2000 })
      .should("equal", "/create");

    cy.createBulkProject();
  });

  describe("I can view projects being imported", () => {
    it("Shows a list of imported projects", () => {
      cy.clickButtonWithName("Project Uploads");

      cy.withinTableRows(DataCy.jobTable, (tr) => {
        tr.should("have.length.above", 1);
      });
    });
  });

  describe("I can see the current import status of a project being imported", () => {
    it("Shows in progress jobs", () => {
      cy.getCy(DataCy.jobStatus, "first").should("contain.text", "In Progress");
    });

    it("Shows completed jobs", () => {
      cy.getCy(DataCy.jobStatus, "first", 20000).should(
        "contain.text",
        "Completed"
      );
    });
  });

  // describe("I can see the current import progress of a project being imported");

  describe("I can delete a project import", () => {
    it("Deletes a project from the list", () => {
      cy.clickButton(DataCy.jobDeleteButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  // describe("I can cancel a project that is being imported");
});
