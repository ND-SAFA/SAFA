import { DataCy, validUser } from "../../fixtures";

describe("Artifact Table Column CRUD", () => {
  beforeEach(() => {
    cy.visit("/login").login(validUser.email, validUser.password);
    cy.location("pathname", { timeout: 10000 }).should("equal", "/account");
  });

  describe("I can add a new table column", () => {
    //TODO: Add tests for adding a new table column
  });

  describe("I can edit a table column", () => {
    //TODO: Add tests for editing a table column
  });

  describe("I can delete a table column", () => {
    //TODO: Add tests for deleting a table column
  });

  describe("I can change the order of my table columns", () => {
    //TODO: Add tests for changing the order of my table columns
  });
});
