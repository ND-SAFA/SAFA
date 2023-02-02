import { DataCy } from "../../../fixtures";

describe("Trace Link Prediction", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject().openApproveGeneratedTraceLinks();
  });

  describe("I can generate a list of trace links using a trained model", () => {
    //TODO: Not really sure how to test this but idk
    it("Can generate a list of trace links using a trained model", () => {});
  });
});
