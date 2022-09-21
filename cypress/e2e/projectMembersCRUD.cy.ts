import { DataCy } from "../fixtures";

describe("Project Members CRUD", () => {
  beforeEach(() => {
    cy.dbResetJobs().createProjectSettings();
  });
  describe("As an owner, I can add a new member to a project", () => {
    it("Cant add an invalid member", () => {
      cy.clickButton(DataCy.selectorAddButton)
        .getCy(DataCy.projectSettingsAddEmail)
        .type("Adrian Rodriguez")
        .clickButtonWithName("Project Role")
        .clickButtonWithName("Viewer");
      cy.getCy(DataCy.projectSettingsAddToProjectButton).should("be.disabled");
    });
    it("Adds a new member to a project", () => {
      cy.addingNewMember("Adrian.R6driguez@gmail.com", "Editor");
    });
  });
  describe("As an owner, I can edit a project members permissions", () => {
    it("Edits the permissions of a project member", () => {
      cy.addingNewMember("Adrian.R6driguez@gmail.com", "Editor");
      cy.clickButton(DataCy.selectorEditButton);

      //below is the command I cant seem to find (its essentially the Project-Role button)
      cy.clickButton(DataCy.projectSettingsProjectRole);
      cy.clickButtonWithName("Viewer");
    });
  });
  describe("As an owner, I can remove a member from a project", () => {
    it("Removes a project member", () => {
      cy.addingNewMember("Adrian.R6driguez@gmail.com", "Editor");

      cy.addingNewMember("Test@test.com", "Admin");

      cy.clickButton(DataCy.selectorDeleteButton).clickButtonWithName(
        "I accept"
      );
    });
  });
});
