import { Routes } from "@/fixtures";

describe("Custom Attributes", () => {
  before(() => {
    cy.initEmptyProject();

    cy.expandViewport()
      .visit(Routes.MY_PROJECTS)
      .locationShouldEqual(Routes.MY_PROJECTS);
  });
});
