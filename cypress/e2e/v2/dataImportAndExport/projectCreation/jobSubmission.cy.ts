import { Routes, validUser, DataCy } from "@/fixtures";

describe("Job Submission", () => {
  beforeEach(() => {
    cy.dbResetJobs().dbResetProjects();

    cy.visit(Routes.PROJECT_CREATOR)
      .login(validUser.email, validUser.password)
      .locationShouldEqual(Routes.PROJECT_CREATOR);

    cy.createBulkProject();
  });

  describe("I can create a job", () => {
    it("Shows the current job is completed", () => {
      cy.waitForJobLoad();
    });
  });

  describe("I can see the jobs I created", () => {
    it("Shows a list of imported projects", () => {
      cy.clickButtonWithName("Project Uploads");

      cy.withinTableRows(DataCy.jobTable, (tr) => {
        tr.should("have.length.above", 1);
      });
    });
  });

  describe("I can delete a logged job", () => {
    it("Deletes a project from the list", () => {
      cy.clickButton(DataCy.jobDeleteButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });
});
