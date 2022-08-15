import { validUser } from "../fixtures";

describe("Project Selection", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080/create").login(
      validUser.email,
      validUser.password
    );
  });

  afterEach(() => {
    cy.logout();
  });

  // it("does something", () => {});
});
