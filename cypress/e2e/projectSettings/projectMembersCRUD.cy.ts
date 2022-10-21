import { DataCy } from "../../fixtures";

describe("Project Members CRUD", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().createProjectSettings();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
    cy.openProjectSettings();
  });

  describe("As an owner, I can add a new member to a project", () => {
    it("Can't add an invalid member", () => {
      cy.projectAddNewMember("test@test.cm", "Viewer");
      cy.getCy(DataCy.snackbarError).should("be.visible");
    });

    it("Can add a new member to the project", () => {
      cy.projectAddNewMember("test2@test.com", "Viewer");
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });
  describe("As an owner, I can edit a project member’s permissions", () => {
    it("Can edit the permissions of a project member", () => {
      cy.clickButton(DataCy.projectSettingsEditUserButton);
      cy.getCy(DataCy.projectSettingsAddRole)
        .click({ force: true })
        .type("Admin", { force: true })
        .type("{enter}", { force: true });
      cy.clickButton(DataCy.projectSettingsAddToProject);
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("As an owner, I can remove a member from a project", () => {
    it("Can remove a member from a project", () => {
      cy.clickButton(DataCy.projectSettingsDeleteUserButton);
      cy.clickButton(DataCy.projectSettingsIAcceptButton);
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });
});
