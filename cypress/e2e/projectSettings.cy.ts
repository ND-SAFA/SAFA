import { validUser } from "../fixtures";

describe.skip("Project Settings", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080/settings").login(
      validUser.email,
      validUser.password
    );
  });

  afterEach(() => {
    cy.logout();
  });

  // it("does something", () => {});
});
