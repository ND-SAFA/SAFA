import { validUser } from "../fixtures";

describe("Project Documents", () => {
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
