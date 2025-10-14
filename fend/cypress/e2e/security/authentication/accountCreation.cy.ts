import { DataCy, Routes } from "@/fixtures";

const { createUser, validUser } = Cypress.env();

describe("Account Creation", () => {
  beforeEach(() => {
    cy.visit(Routes.LOGIN_ACCOUNT);
  });

  describe("I can create an account with an unused email", () => {
    it("Creates an account successfully", () => {
      cy.clickButton(DataCy.createAccountPageButton).locationShouldEqual(
        Routes.CREATE_ACCOUNT
      );

      cy.inputText(DataCy.newAccountEmailInput, createUser.email)
        .inputText(DataCy.newAccountPasswordInput, createUser.password)
        .clickButton(DataCy.createAccountButton);

      cy.contains("p", "Your account has been successfully created.").should(
        "be.visible"
      );

      cy.dbDeleteUser(createUser.email, createUser.password);
    });
  });

  describe("I cant create an account with an email that has already been used", () => {
    it("Disables account creation", () => {
      cy.clickButton(DataCy.createAccountPageButton).locationShouldEqual(
        Routes.CREATE_ACCOUNT
      );

      cy.inputText(DataCy.newAccountEmailInput, validUser.email)
        .inputText(DataCy.newAccountPasswordInput, validUser.password)
        .clickButton(DataCy.createAccountButton);

      cy.contains("Unable to create an account").should("be.visible");
    });
  });
});
