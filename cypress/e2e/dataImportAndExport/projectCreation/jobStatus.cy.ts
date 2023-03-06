import { DataCy, Routes } from "@/fixtures";

describe("Job Status", () => {
  beforeEach(() => {
    cy.initProject(false);

    cy.locationShouldEqual(Routes.UPLOAD_STATUS);
  });

  afterEach(() => {
    cy.waitForJobLoad();
  });

  describe("I can see the current status of a job", () => {
    it("Shows in progress jobs", () => {
      cy.getCy(DataCy.jobStatus, "first").should("contain.text", "In Progress");
    });

    it("Shows completed jobs", () => {
      cy.getCy(DataCy.jobStatus, "first", 10000).should(
        "contain.text",
        "Completed"
      );
    });
  });

  describe("I can see the current progress of a job", () => {
    it("Shows in progress jobs", () => {
      cy.getCy(DataCy.jobProgress, "first", 10000).should(
        "contain.text",
        "75%"
      );
    });

    it("Shows completed jobs", () => {
      cy.getCy(DataCy.jobProgress, "first", 10000).should(
        "contain.text",
        "100%"
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
