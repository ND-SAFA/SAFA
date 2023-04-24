import { Routes, DataCy } from "@/fixtures";
import { user } from "@/fixtures/data/user";

describe("Account Editing", () => {
  describe("I can edit my password while logged in", () => {
    beforeEach(() => {
      cy.loginToPage(
        user.editUser.email,
        user.editUser.password,
        Routes.ACCOUNT
      );
    });

    it("Should not be able to change my password without an old and new password set", () => {
      cy.getCy(DataCy.passwordChangeButton).should("be.disabled");
    });

    it("Should not be able to change my password with an invalid current password", () => {
      cy.inputText(DataCy.passwordCurrentInput, user.invalidUser.password)
        .inputText(DataCy.passwordNewInput, user.editUser.newPassword)
        .clickButton(DataCy.passwordChangeButton);

      cy.getCy(DataCy.snackbarError).should("be.visible");

      // Test that the password was not changed.
      cy.logout();
      cy.login(user.editUser.email, user.editUser.newPassword);
      cy.locationShouldEqual(Routes.LOGIN_ACCOUNT);
      cy.contains("Invalid username or password");
    });

    it("Should be able to change my password with the correct current password", () => {
      // Set the password to a new value.
      cy.inputText(DataCy.passwordCurrentInput, user.editUser.password)
        .inputText(DataCy.passwordNewInput, user.editUser.newPassword)
        .clickButton(DataCy.passwordChangeButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      // Test that the password was changed.
      cy.logout()
        .visit(Routes.ACCOUNT)
        .login(user.editUser.email, user.editUser.newPassword)
        .locationShouldEqual(Routes.ACCOUNT);

      // Revert the password value.
      cy.inputText(DataCy.passwordCurrentInput, user.editUser.newPassword)
        .inputText(DataCy.passwordNewInput, user.editUser.password)
        .clickButton(DataCy.passwordChangeButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("I can delete my account", () => {
    it("Cannot delete my account with an invalid password", () => {
      cy.loginToPage(
        user.editUser.email,
        user.editUser.password,
        Routes.ACCOUNT
      );

      cy.inputText(DataCy.accountDeletePasswordInput, user.invalidUser.password)
        .clickButton(DataCy.accountDeleteButton)
        .clickButton(DataCy.confirmModalButton);

      cy.getCy(DataCy.snackbarError).should("be.visible");
      cy.logout()
        .login(user.editUser.email, user.editUser.password)
        .should("not.contain", "Invalid username or password");
    });

    it("Successfully deletes my account", () => {
      cy.createNewAccount(user.deleteUser.email, user.deleteUser.password);

      cy.loginToPage(
        user.deleteUser.email,
        user.deleteUser.password,
        Routes.ACCOUNT
      );

      cy.inputText(DataCy.accountDeletePasswordInput, user.deleteUser.password)
        .clickButton(DataCy.accountDeleteButton)
        .clickButton(DataCy.confirmModalButton);

      cy.locationShouldEqual(Routes.LOGIN_ACCOUNT);

      // Try to login with the deleted account.
      cy.login(user.deleteUser.email, user.deleteUser.password);
      cy.contains("Invalid username or password");
    });
  });
});
