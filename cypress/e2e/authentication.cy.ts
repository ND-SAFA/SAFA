import { validUser, invalidUser } from "../fixtures/user.json";

describe("Authentication", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080");
  });

  describe("I can create an account", () => {
    it("displays successful account creation", () => {
      cy.clickButton("Sign Up").wait(500);

      cy.inputText("Email", validUser.email)
        .inputText("Password", validUser.password)
        .clickButton("Create Account");

      cy.contains(
        "p",
        "Your account has been successfully created. Please check your email to complete the sign up process."
      );
    });
  });

  describe("I can log in", () => {
    it("logs in successfully with validUser credentials", () => {
      cy.login(validUser.email, validUser.password);

      cy.get("#account-dropdown").should("exist");
    });

    it("fails to log in with invalidUser credentials", () => {
      cy.login(invalidUser.email, invalidUser.password);

      cy.get("#account-dropdown").should("not.exist");
    });

    it("wont let you log in without both an email and password", () => {
      cy.inputText("Email", validUser.email);

      cy.getButton("Login").should("be.disabled");
    });
  });

  describe("I can log out", () => {
    it("logs out successfully", () => {
      cy.login(validUser.email, validUser.password);
      cy.logout();
      cy.getButton("Login").should("exist");
    });

    it("clears my session on logout", () => {
      cy.login(validUser.email, validUser.password);
      cy.logout();

      const store = JSON.parse(localStorage.getItem("vuex"));

      expect(store).to.deep.equal({
        session: { session: { token: "", versionId: "" } },
      });
    });
  });
});
