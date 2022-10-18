import { validUser } from "../fixtures";

describe.skip("Artifact Table", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080/project").login(
      validUser.email,
      validUser.password
    );
  });

  afterEach(() => {
    cy.logout();
  });

  // it("does something", () => {});
});
