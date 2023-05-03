import { DataCy, Routes } from "@/fixtures";

const { invalidUser, validUser } = Cypress.env();

describe("Account Login", () => {
  beforeEach(() => {
    cy.visit(Routes.LOGIN_ACCOUNT);
  });

  describe("I cannot enter credentials without both an email and password", () => {
    it("Disables login", () => {
      cy.inputText(DataCy.emailInput, validUser.email);

      cy.getCy(DataCy.loginButton).should("be.disabled");
    });
  });

  describe("I cant log in with invalid credentials", () => {
    it("Fails to log in", () => {
      cy.inputText(DataCy.emailInput, invalidUser.email).inputText(
        DataCy.passwordInput,
        invalidUser.password
      );

      cy.getCy(DataCy.isLoggedIn).should("not.exist");
    });
  });

  describe("I can log in with valid credentials", () => {
    it("Logs in successfully", () => {
      cy.login(validUser.email, validUser.password);

      cy.getCy(DataCy.isLoggedIn).should("exist");
    });
  });

  describe("I can log out", () => {
    it("Logs out successfully", () => {
      cy.login(validUser.email, validUser.password).logout();

      cy.getCy(DataCy.loginButton).should("exist");

      cy.visit(Routes.ACCOUNT);

      cy.getCy(DataCy.loginButton).should("exist");
    });
  });

  // describe.skip("When I log out, all stored project information is cleared", () => {});
});
