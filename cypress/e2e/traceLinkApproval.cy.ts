import { validUser } from "../fixtures";

describe("Trace Link Approval", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080/links").login(
      validUser.email,
      validUser.password
    );
  });

  afterEach(() => {
    cy.logout();
  });

  // it("does something", () => {});
});
