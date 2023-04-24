import { DataCy, Routes } from "@/fixtures";
import { user } from "@/fixtures/data/user";
describe("Account Login", () => {
  beforeEach(() => {
    cy.visit(Routes.LOGIN_ACCOUNT);
  });

  describe("I cannot enter credentials without both an email and password", () => {
    it("Disables login", () => {
      cy.inputText(DataCy.emailInput, user.validUser.email);

      cy.getCy(DataCy.loginButton).should("be.disabled");
    });
  });

  describe("I cant log in with invalid credentials", () => {
    it("Fails to log in", () => {
      cy.inputText(DataCy.emailInput, user.invalidUser.email).inputText(
        DataCy.passwordInput,
        user.invalidUser.password
      );

      cy.getCy(DataCy.isLoggedIn).should("not.exist");
    });
  });

  describe("I can log in with valid credentials", () => {
    it("Logs in successfully", () => {
      cy.login(user.validUser.email, user.validUser.password);

      cy.getCy(DataCy.isLoggedIn).should("exist");
    });
  });

  describe("I can log out", () => {
    it("Logs out successfully", () => {
      cy.login(user.validUser.email, user.validUser.password).logout();

      cy.getCy(DataCy.loginButton).should("exist");

      cy.visit(Routes.ACCOUNT);

      cy.getCy(DataCy.loginButton).should("exist");
    });
  });

  describe.skip("When I log out, all stored project information is cleared", () => {});
});
