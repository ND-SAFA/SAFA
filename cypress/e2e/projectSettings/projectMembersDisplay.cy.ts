import { DataCy } from "../../fixtures";
import "cypress-wait-until";

describe("Project Members Display", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().createProjectSettings();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
    cy.projectSettingsSelector();
    cy.projectAddNewMember("test2@test.com", "Admin");
    cy.waitUntil(function () {
      return cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("I can search through a project’s members", () => {
    it("Can search for a specific member", () => {
      cy.getCy(DataCy.projectSettingsSearchUser).first().type("test2");
      cy.getCy(DataCy.projectSettingsTable)
        .find('td:contains("test2")')
        .should("have.length", 1);
    });
  });

  describe("I can see a project’s members", () => {
    it("Can display all project members", () => {
      cy.getCy(DataCy.projectSettingsTable)
        .find("tr")
        // There should be 3 (Heading, owner, and added user)
        .should("have.length", 3);
    });
  });
});
