import { validUser } from "../fixtures/user.json";

describe("Artifact Graph", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080/create").login(
      validUser.email,
      validUser.password
    );
  });

  // it("does something", () => {});
});
