import { DataCy } from "@/fixtures";

describe("Job Submission", () => {
  beforeEach(() => {
    cy.viewport(1080, 1080);
    cy.initProject(false);
  });

  describe("I can create a job", () => {
    it("Shows the current job is completed", () => {
      cy.waitForJobLoad();
    });
  });

  describe("I can see the jobs I created", () => {
    it("Shows a list of imported projects", () => {
      cy.clickButtonWithName("Project Uploads");
      cy.waitForJobLoad();

      cy.withinTableRows(
        DataCy.jobTable,
        (tr) => {
          tr.should("have.length.above", 1);
        },
        false
      );
    });
  });

  describe("I can delete a logged job", () => {
    it.only("Deletes a project from the list", () => {
      cy.waitForJobLoad();

      cy.clickButton(DataCy.jobDeleteButton);

      cy.withinTableRows(
        DataCy.jobTable,
        (tr) => {
          tr.should("have.length", 1);
        },
        false
      );

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });
});
