import { DataCy, Routes } from "@/fixtures";
import { user } from "@/support/e2e";

describe("Account Creation", () => {
  beforeEach(() => {
    cy.visit(Routes.LOGIN_ACCOUNT);
  });

  describe("I can create an account with an unused email", () => {
    it("Creates an account successfully", () => {
      cy.clickButton(DataCy.createAccountPageButton).locationShouldEqual(
        Routes.CREATE_ACCOUNT
      );

      cy.inputText(DataCy.newAccountEmailInput, user.createUser.email)
        .inputText(DataCy.newAccountPasswordInput, user.createUser.password)
        .clickButton(DataCy.createAccountButton);

      cy.contains("p", "Your account has been successfully created.").should(
        "be.visible"
      );

      cy.dbDeleteUser(user.createUser.email, user.createUser.password);
    });
  });

  describe("I cant create an account with an email that has already been used", () => {
    it("Disables account creation", () => {
      cy.clickButton(DataCy.createAccountPageButton).locationShouldEqual(
        Routes.CREATE_ACCOUNT
      );

      cy.inputText(DataCy.newAccountEmailInput, user.validUser.email)
        .inputText(DataCy.newAccountPasswordInput, user.validUser.password)
        .clickButton(DataCy.createAccountButton);

      cy.contains("Unable to create an account").should("be.visible");
    });
  });
});
