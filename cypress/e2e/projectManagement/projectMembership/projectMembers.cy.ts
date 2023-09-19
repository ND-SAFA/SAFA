import { DataCy } from "@/fixtures";

const inviteUser = Cypress.env("inviteUser");

describe("Project Members", () => {
  beforeEach(() => {
    cy.initEmptyProject()
      .initProjectVersion(false)
      .openProjectSettings()
      .switchTab("Members");
  });

  describe("As an owner, I can add a new member to a project", () => {
    it("Can't add an invalid member", () => {
      cy.projectAddNewMember(inviteUser.invalidEmail, "Viewer");

      cy.getCy(DataCy.snackbarError).should("be.visible");
    });

    it("Can add a new member to the project", () => {
      cy.projectAddNewMember(inviteUser.email, "Viewer");

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  // TODO: enable when member editing is fixed
  describe.skip("As an owner, I can edit a project member’s permissions", () => {
    it("Can edit the permissions of a project member", () => {
      cy.projectAddNewMember(inviteUser.email, "Viewer");
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.clickButton(
        DataCy.projectSettingsSwitchRole,
        "last"
      ).clickButtonWithName("Editor");

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("As an owner, I can remove a member from a project", () => {
    it("Can remove a member from a project", () => {
      cy.projectAddNewMember(inviteUser.email, "Viewer");

      cy.clickButton(
        DataCy.projectSettingsDeleteUserButton,
        "last"
      ).clickButton(DataCy.confirmModalButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });
});
