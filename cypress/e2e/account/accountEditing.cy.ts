import { DataCy, editUser } from "../../fixtures";

describe("Account Editing", () => {
  before(() => {
    cy.visit("/create-account").createNewAccount(
      editUser.email,
      editUser.password
    );
  });

  beforeEach(() => {
    cy.visit("/account")
      .login(editUser.email, editUser.password)
      .location("pathname", { timeout: 10000 })
      .should("equal", "/account");
  });

  describe("Password Change", () => {
    describe("I can edit my password while logged in", () => {
      it("Should not be able to change my password without an old and new password set", () => {
        cy.getCy(DataCy.passwordChangeButton).should("be.disabled");
      });

      it("Should not be able to change my password with an invalid current password", () => {
        cy.inputText(DataCy.passwordCurrentInput, editUser.invalidPassword);
        cy.inputText(DataCy.passwordNewInput, editUser.newPassword);
        cy.getCy(DataCy.passwordChangeButton).click();
        cy.getCy(DataCy.snackbarError).should("be.visible");
      });

      it("Should be able to change my password with the correct current password", () => {
        cy.inputText(DataCy.passwordCurrentInput, editUser.password);
        cy.inputText(DataCy.passwordNewInput, editUser.newPassword);
        cy.getCy(DataCy.passwordChangeButton).click();
        cy.getCy(DataCy.snackbarSuccess).should("be.visible");

        // For now, we will change the password back to the original password
        cy.inputText(DataCy.passwordCurrentInput, editUser.newPassword);
        cy.inputText(DataCy.passwordNewInput, editUser.password);
        cy.getCy(DataCy.passwordChangeButton).click();
        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      });
    });

    describe("I can delete my account", () => {
      it("Cannot delete my account with an invalid password", () => {
        cy.inputText(
          DataCy.accountDeletePasswordInput,
          editUser.invalidPassword
        );
        cy.getCy(DataCy.accountDeleteButton).click();
        cy.getCy(DataCy.popUpAcceptButton).click();
        cy.location("pathname", { timeout: 5000 }).should(
          "not.equal",
          "/login"
        );
      });

      it.skip("Successfully deletes my account", () => {
        cy.inputText(DataCy.accountDeletePasswordInput, editUser.password);
        cy.getCy(DataCy.accountDeleteButton).click();
        cy.getCy(DataCy.popUpAcceptButton).click();
        cy.location("pathname", { timeout: 5000 }).should("equal", "/login");
      });
    });
  });
});
