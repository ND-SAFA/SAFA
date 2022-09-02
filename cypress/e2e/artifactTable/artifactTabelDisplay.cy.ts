import { DataCy, validUser } from "../../fixtures";

describe("Artifact Table Display", () => {
  beforeEach(() => {
    cy.visit("/login").login(validUser.email, validUser.password);
    cy.location("pathname", { timeout: 10000 }).should("equal", "/account");
  });

  describe("I can sort artifacts by their attributes", () => {
    //TODO: Add tests for sorting artifacts by their attributes
  });

  describe("I can group artifacts by their attributes", () => {
    //TODO: Add tests for grouping artifacts by their attributes
  });

  describe("I can see project warnings in the artifact table", () => {
    //TODO: Add tests for seeing project warnings in the artifact table
  });
});
