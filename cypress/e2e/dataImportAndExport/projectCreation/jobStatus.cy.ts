import { DataCy, Routes } from "@/fixtures";

// TODO: remove this workaround once websocket messages are fixed.
describe.skip("Job Status", () => {
  beforeEach(() => {
    cy.viewport(1080, 1080);
    cy.initProject(false);
    cy.locationShouldEqual(Routes.UPLOAD_STATUS);
  });

  afterEach(() => {
    cy.waitForJobLoad();
  });

  describe("I can see the current status and progress of a job", () => {
    it("Shows in progress jobs", () => {
      cy.contains("Project Uploads");
      cy.getCy(DataCy.jobStatus, "first").should("contain.text", "In Progress");
    });

    it("Shows completed jobs", () => {
      cy.getCy(DataCy.jobStatus, "first", 10000).should(
        "contain.text",
        "Completed"
      );
    });
  });

  describe("I can see real-time job updates", () => {
    it("Shows the progress updating", () => {
      cy.getCy(DataCy.jobOpenButton, "first", 10000).should("be.disabled");
      cy.getCy(DataCy.jobOpenButton, "first", 10000).should("not.be.disabled");
    });
  });

  describe("I can see the logs occurring during my job", () => {
    it("Shows the job logs", () => {
      cy.clickButton(DataCy.jobLogButton, "first");

      cy.getCy(DataCy.jobLogText).should("be.visible");
    });
  });
});
