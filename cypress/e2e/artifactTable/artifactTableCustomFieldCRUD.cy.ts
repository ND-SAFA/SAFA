import { DataCy, validUser } from "../../fixtures";

describe("Artifact Table Custom Field CRUD", () => {
  beforeEach(() => {
    cy.visit("/login").login(validUser.email, validUser.password);
    cy.location("pathname", { timeout: 10000 }).should("equal", "/account");
  });

  describe("In a table document, I can edit an artifact’s custom fields", () => {
    //TODO: Add tests for editing an artifact’s custom fields
  });

  describe("I can edit the contents of a custom field in line", () => {
    //TODO: Add tests for editing the contents of a custom field in line
  });
});
