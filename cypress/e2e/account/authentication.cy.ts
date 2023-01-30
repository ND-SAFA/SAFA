import { validUser, invalidUser, DataCy } from "../../fixtures";

describe("Authentication", () => {
  // TODO: Fix the dbDeleteUser command
  // before(() => {
  //   cy.dbDeleteUser("newAccount@new.com");
  // });

  beforeEach(() => {
    cy.visit("/login");
  });

  // Disabled until account deletion is added, or until running in a test DB
  describe("Account Creation", () => {
    describe.skip("I can create an account", () => {
      it("displays successful account creation", () => {
        cy.clickButton("button-create-account-redirect").wait(500);

        cy.inputText(DataCy.newAccountEmailInput, "newAccount@new.com")
          .inputText(DataCy.newAccountPasswordInput, "newPassword")
          .clickButton("button-create-account");

        cy.contains(
          "p",
          "Your account has been successfully created. Please check your email to complete the sign up process."
        );
      });
    });
  });

  describe("Account Login", () => {
    describe("I can log in", () => {
      it("logs in successfully with validUser credentials", () => {
        cy.login(validUser.email, validUser.password);

        cy.getCy(DataCy.isLoggedIn).should("exist");
      });

      it("fails to log in with invalidUser credentials", () => {
        cy.inputText(DataCy.emailInput, invalidUser.email).inputText(
          DataCy.passwordInput,
          invalidUser.password
        );

        cy.getCy(DataCy.isLoggedIn).should("not.exist");
      });

      it("wont let you log in without both an email and password", () => {
        cy.inputText(DataCy.emailInput, validUser.email);

        cy.getCy(DataCy.loginButton).should("be.disabled");
      });
    });

    describe("I can log out", () => {
      it("logs out successfully", () => {
        cy.login(validUser.email, validUser.password).logout();

        cy.getCy(DataCy.loginButton).should("exist");

        // cy.visit("/");

        // cy.getCy(DataCy.loginButton).should("exist");
      });
    });
  });
});
