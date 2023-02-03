import { Routes, editUser, DataCy } from "@/fixtures";

describe("Account Editing", () => {
  describe("I can edit my password while logged in", () => {
    before(() => {
      cy.dbDeleteUser(editUser.email, editUser.password).createNewAccount(
        editUser.email,
        editUser.password
      );
    });

    beforeEach(() => {
      cy.loginToPage(editUser.email, editUser.password, Routes.ACCOUNT);
    });

    it("Should not be able to change my password without an old and new password set", () => {
      cy.getCy(DataCy.passwordChangeButton).should("be.disabled");
    });

    it("Should not be able to change my password with an invalid current password", () => {
      cy.inputText(DataCy.passwordCurrentInput, editUser.invalidPassword)
        .inputText(DataCy.passwordNewInput, editUser.newPassword)
        .clickButton(DataCy.passwordChangeButton);

      cy.getCy(DataCy.snackbarError).should("be.visible");
    });

    it("Should be able to change my password with the correct current password", () => {
      // Set the password to a new value.
      cy.inputText(DataCy.passwordCurrentInput, editUser.password)
        .inputText(DataCy.passwordNewInput, editUser.newPassword)
        .clickButton(DataCy.passwordChangeButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      // Revert the password value.
      cy.inputText(DataCy.passwordCurrentInput, editUser.newPassword)
        .inputText(DataCy.passwordNewInput, editUser.password)
        .clickButton(DataCy.passwordChangeButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("I can delete my account", () => {
    beforeEach(() => {
      cy.createNewAccount(editUser.email, editUser.password);

      cy.loginToPage(editUser.email, editUser.password, Routes.ACCOUNT);
    });

    it("Cannot delete my account with an invalid password", () => {
      cy.inputText(DataCy.accountDeletePasswordInput, editUser.invalidPassword)
        .clickButton(DataCy.accountDeleteButton)
        .clickButton(DataCy.confirmModalButton);

      cy.getCy(DataCy.snackbarError).should("be.visible");

      cy.dbDeleteUser(editUser.email, editUser.password);
    });

    it("Successfully deletes my account", () => {
      cy.inputText(DataCy.accountDeletePasswordInput, editUser.password)
        .clickButton(DataCy.accountDeleteButton)
        .clickButton(DataCy.confirmModalButton);

      cy.locationShouldEqual(Routes.LOGIN_ACCOUNT);
    });
  });
});
