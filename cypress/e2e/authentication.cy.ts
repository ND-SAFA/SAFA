const validTestUser = {
  email: "tjnewman111@gmail.com",
  password: "123",
};

const invalidTestUser = {
  email: "tjnewman111@gmail.com",
  password: "321",
};

describe("Authentication", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080");
  });

  describe("I can log in", () => {
    it("logs in successfully with valid credentials", () => {
      cy.login(validTestUser.email, validTestUser.password);

      cy.get("#account-dropdown").should("exist");
    });

    it("fails to log in with invalid credentials", () => {
      cy.login(invalidTestUser.email, invalidTestUser.password);

      cy.get("#account-dropdown").should("not.exist");
    });

    it("wont let you log in without both an email and password", () => {
      cy.inputText("Email", validTestUser.email);

      cy.getButton("Login").should("be.disabled");
    });
  });

  describe("I can log out", () => {
    it("logs out successfully", () => {
      cy.login(validTestUser.email, validTestUser.password);
      cy.logout();
      cy.getButton("Login").should("exist");
    });

    it("clears my session on logout", () => {
      cy.login(validTestUser.email, validTestUser.password);
      cy.logout();

      const store = JSON.parse(localStorage.getItem("vuex"));

      expect(store).to.deep.equal({
        session: { session: { token: "", versionId: "" } },
      });
    });
  });
});
