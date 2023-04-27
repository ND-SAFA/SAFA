import { DataCy } from "@/fixtures";
const user = Cypress.env();
describe("Project Members", () => {
  beforeEach(() => {
    cy.initEmptyProject().initProjectVersion(false).openProjectSettings();
  });

  describe("As an owner, I can add a new member to a project", () => {
    it("Can't add an invalid member", () => {
      cy.projectAddNewMember(user.inviteUser.invalidEmail, "Viewer");

      cy.getCy(DataCy.snackbarError).should("be.visible");
    });

    it("Can add a new member to the project", () => {
      cy.projectAddNewMember(user.inviteUser.email, "Viewer");

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("As an owner, I can edit a project member’s permissions", () => {
    it("Can edit the permissions of a project member", () => {
      cy.projectAddNewMember(user.inviteUser.email, "Viewer");

      cy.clickButton(DataCy.projectSettingsEditUserButton, "last");

      cy.clickButton(DataCy.projectSettingsAddRole).clickButtonWithName(
        "Admin"
      );

      cy.clickButton(DataCy.projectSettingsAddToProject);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("As an owner, I can remove a member from a project", () => {
    it("Can remove a member from a project", () => {
      cy.projectAddNewMember(user.inviteUser.email, "Viewer");

      cy.clickButton(
        DataCy.projectSettingsDeleteUserButton,
        "last"
      ).clickButton(DataCy.confirmModalButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });
});
