import { validUser, invalidUser, DataCy } from "../fixtures";

describe("Authentication", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080");
  });

  // Disabled until account deletion is added, or until running in a test DB
  // describe("Account Creation", () => {
  //   describe("I can create an account", () => {
  //     it("displays successful account creation", () => {
  //       cy.clickButton("button-create-account-redirect").wait(500);
  //
  //       cy.inputText(DataCy.emailInput, validUser.email)
  //         .inputText(DataCy.passwordInput, validUser.password)
  //         .clickButton("button-create-account");
  //
  //       cy.contains(
  //         "p",
  //         "Your account has been successfully created. Please check your email to complete the sign up process."
  //       );
  //     });
  //   });
  // });

  describe("Account Login", () => {
    describe("I can log in", () => {
      it("logs in successfully with validUser credentials", () => {
        cy.login(validUser.email, validUser.password);

        cy.getCy(DataCy.accountDropdown).should("exist");
      });

      it("fails to log in with invalidUser credentials", () => {
        cy.login(invalidUser.email, invalidUser.password);

        cy.getCy(DataCy.accountDropdown).should("not.exist");
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
      });

      it("clears my session on logout", () => {
        cy.login(validUser.email, validUser.password)
          .logout()
          .visit("http://localhost:8080");

        cy.getCy(DataCy.loginButton).should("exist");
      });
    });
  });
});
