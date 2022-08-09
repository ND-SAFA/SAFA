import { validUser, invalidUser } from "../fixtures/user.json";

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
  //       cy.inputText("input-email", validUser.email)
  //         .inputText("input-password", validUser.password)
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

        cy.get("[data-cy='account-dropdown']").should("exist");
      });

      it("fails to log in with invalidUser credentials", () => {
        cy.login(invalidUser.email, invalidUser.password);

        cy.get("[data-cy='account-dropdown']").should("not.exist");
      });

      it("wont let you log in without both an email and password", () => {
        cy.inputText("input-email", validUser.email);

        cy.getCy("button-login").should("be.disabled");
      });
    });

    describe("I can log out", () => {
      it("logs out successfully", () => {
        cy.login(validUser.email, validUser.password);
        cy.logout();
        cy.getCy("button-login").should("exist");
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
});
