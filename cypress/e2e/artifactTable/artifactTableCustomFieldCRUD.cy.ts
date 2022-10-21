import { DataCy, validUser } from "../../fixtures";

describe("Artifact Table Custom Field CRUD", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
    cy.switchToTableView();
  });

  describe("In a table document, I can edit an artifact’s custom fields", () => {
    //TODO: Add tests for editing an artifact’s custom fields
  });

  describe("I can edit the contents of a custom field in line", () => {
    //TODO: Add tests for editing the contents of a custom field in line
  });
});
