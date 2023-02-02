import { Routes } from "@/fixtures";

describe("Project Members", () => {
  before(() => {
    cy.initEmptyProject();

    cy.expandViewport()
      .visit(Routes.MY_PROJECTS)
      .locationShouldEqual(Routes.MY_PROJECTS);
  });
});
