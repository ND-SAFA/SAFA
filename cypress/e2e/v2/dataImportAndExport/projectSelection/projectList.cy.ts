import { DataCy, Routes, testProject, validUser } from "@/fixtures";

describe("Project List", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects();
    cy.loadNewProject();
  });

  beforeEach(() => {
    cy.expandViewport()
      .visit(Routes.MY_PROJECTS)
      .login(validUser.email, validUser.password)
      .locationShouldEqual(Routes.MY_PROJECTS);
  });

  describe("I can search for projects by name", () => {
    it("Filters for projects that match my search", () => {
      cy.inputText(DataCy.selectionSearch, testProject.name);

      cy.withinTableRows(DataCy.selectionProjectList, (tr) =>
        tr.should("contain.text", testProject.name)
      );
    });

    it("Displays no projects when none match", () => {
      cy.inputText(DataCy.selectionSearch, "$".repeat(20));

      cy.withinTableRows(DataCy.selectionProjectList, (tr) => {
        tr.should("have.length", 2);
      });
    });
  });

  describe("I can select a project to see its versions", () => {
    it("Selects a project and continues to the version step", () => {
      cy.projectSelectorContinue("project");

      cy.getCy(DataCy.stepperBackButton).should("not.be.disabled");
    });

    it("Cannot continue without a project selected", () => {
      cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
    });
  });
});
