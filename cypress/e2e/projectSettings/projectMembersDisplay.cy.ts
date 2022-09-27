import { DataCy } from "../../fixtures";

describe("Porject members display", () => {
  before(() => {
    cy.dbResetJobs().createProjectSettings();

    cy.addingNewMember("Adrian.R6driguez@gmail.com", "Editor");
  });
  describe("I can search through a projects members", () => {
    it("searches for a specific project member", () => {
      cy.clickButton(DataCy.selectionSearch)
        .type("Adrian.r6driguez@gmail.com")
        .contains("Adrian.R6driguez@gmail.com");
    });
  });
  describe("I can see a projects members", () => {
    it("Displays all members of the project", () => {
      cy.addingNewMember(
        "Adrian.R6driguez@gmail.com",
        "Viewer"
      ).addingNewMember("test@test.com", "Admin");
      cy.clickButton(DataCy.selectionSearch)
        .contains("Adrian.R6driguez.com")
        .contains("test@test.com");
    });
  });
});
