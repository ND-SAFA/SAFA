import {
  simpleProjectFiles,
  simpleProjectFilesMap,
  DataCy,
  testProject,
  Routes,
} from "@/fixtures";

const validUser = Cypress.env("validUser");

describe("Bulk Project Creation", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects();
  });

  beforeEach(() => {
    cy.viewport(1920, 1080);
    cy.loginToPage(
      validUser.email,
      validUser.password,
      Routes.PROJECT_CREATOR,
      { tab: "bulk" }
    );
  });

  describe("I cannot create a project without a name", () => {
    it("Cant create a project without a name", () => {
      cy.inputText(DataCy.creationBulkDescriptionInput, testProject.name);

      cy.getCy(DataCy.creationContinueButton).should("be.disabled");
    });
  });

  describe("I can generate a TIM configuration file", () => {
    it("Generates a missing TIM file", () => {
      cy.setProjectIdentifier("bulk").uploadFiles(
        DataCy.creationBulkFilesInput,
        ...simpleProjectFiles.filter((name) => !name.includes("tim"))
      );

      cy.getCy(DataCy.creationUploadButton).should("be.disabled");

      cy.clickButton(DataCy.creationTimToggle);

      cy.getCy(DataCy.creationTimToggle).within(() =>
        cy
          .getCy(DataCy.creationTimArtifactsInput)
          .parent()
          .click()
          .type("design{downArrow}{enter}")
      );

      cy.getCy(DataCy.creationUploadButton).should("not.be.disabled");
    });
  });

  describe("I can create a project from flat files", () => {
    it("Can create a valid project", () => {
      cy.setProjectIdentifier("bulk")
        .uploadFiles(DataCy.creationBulkFilesInput, ...simpleProjectFiles)
        .clickButton(DataCy.creationUploadButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });
});
