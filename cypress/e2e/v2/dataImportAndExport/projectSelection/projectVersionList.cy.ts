import { DataCy, Routes, validUser } from "@/fixtures";

describe("Project Version List", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects();
    cy.loadNewProject();
  });

  beforeEach(() => {
    cy.expandViewport().loginToPage(
      validUser.email,
      validUser.password,
      Routes.MY_PROJECTS
    );
  });

  describe("I can select and load a version of the project", () => {
    it("Cannot continue if a version is not selected", () => {
      cy.projectSelectorContinue("project");

      cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
    });

    it("Selects and loads a project and version", () => {
      cy.projectSelectorContinue("project").projectSelectorContinue("version");

      cy.getCy(DataCy.appLoading).should("be.visible");
      cy.waitForProjectLoad(true);
    });
  });
});
