import { DataCy } from "../../fixtures";

describe("Trace Link Approval", () => {
  //TODO: Figure out how to test this and structure the test
  // Folow the same before and before each as each other project

  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject().openApproveGeneratedTraceLinks();
  });

  describe("I can approve trace links", () => {
    it("Approves a trace link", () => {
      cy.clickButton("DataCy.traceLinkGenerationApproveAllButton").click();
      cy.getCy("DataCy.traceLinkGenerationApproveAllButton").should(
        "not.exist"
      );
    });
  });
});
