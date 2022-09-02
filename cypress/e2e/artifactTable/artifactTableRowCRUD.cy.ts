import { DataCy, validUser } from "../../fixtures";

describe("Artifact Table Row CRUD", () => {
  beforeEach(() => {
    cy.visit("/login").login(validUser.email, validUser.password);
    cy.location("pathname", { timeout: 10000 }).should("equal", "/account");
  });

  describe("I can add a row to the artifact table", () => {
    //TODO: Add tests for adding a row to the artifact table
  });

  describe("I can edit a row of the artifact table", () => {
    //TODO: Add tests for editing a row of the artifact table
  });

  describe("I can delete a row of the artifact table", () => {
    //TODO: Add tests for deleting a row of the artifact table
  });

  describe("I can see missing required fields in each row", () => {
    //TODO: Add tests for seeing missing required fields in each row
  });
});
