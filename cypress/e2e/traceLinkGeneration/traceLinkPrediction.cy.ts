import { DataCy } from "../../fixtures";

describe("Trace Link Prediction", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject().openApproveGeneratedTraceLinks();
  });
});
