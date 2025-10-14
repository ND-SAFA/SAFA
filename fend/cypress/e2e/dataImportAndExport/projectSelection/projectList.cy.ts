import { DataCy, Routes, testProject } from "@/fixtures";

const validUser = Cypress.env("validUser");

describe("Project List", () => {
  before(() => {
    cy.initEmptyProject().clearAllCookies();
  });

  beforeEach(() => {
    cy.viewport(1080, 1080);
    cy.loginToPage(validUser.email, validUser.password, Routes.MY_PROJECTS);
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
        tr.should("have.length", 1);
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
