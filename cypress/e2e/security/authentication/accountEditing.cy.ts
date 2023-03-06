import { Routes, editUser, invalidUser, deleteUser, DataCy } from "@/fixtures";

describe("Account Editing", () => {
  describe("I can edit my password while logged in", () => {
    beforeEach(() => {
      cy.loginToPage(editUser.email, editUser.password, Routes.ACCOUNT);
    });

    it("Should not be able to change my password without an old and new password set", () => {
      cy.getCy(DataCy.passwordChangeButton).should("be.disabled");
    });

    it("Should not be able to change my password with an invalid current password", () => {
      cy.inputText(DataCy.passwordCurrentInput, invalidUser.password)
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
    it("Cannot delete my account with an invalid password", () => {
      cy.loginToPage(editUser.email, editUser.password, Routes.ACCOUNT);

      cy.inputText(DataCy.accountDeletePasswordInput, invalidUser.password)
        .clickButton(DataCy.accountDeleteButton)
        .clickButton(DataCy.confirmModalButton);

      cy.getCy(DataCy.snackbarError).should("be.visible");
    });

    it("Successfully deletes my account", () => {
      cy.createNewAccount(deleteUser.email, deleteUser.password);

      cy.loginToPage(deleteUser.email, deleteUser.password, Routes.ACCOUNT);

      cy.inputText(DataCy.accountDeletePasswordInput, deleteUser.password)
        .clickButton(DataCy.accountDeleteButton)
        .clickButton(DataCy.confirmModalButton);

      cy.locationShouldEqual(Routes.LOGIN_ACCOUNT);
    });
  });
});
