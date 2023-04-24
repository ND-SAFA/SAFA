import {
  simpleProjectFiles,
  simpleProjectFilesMap,
  DataCy,
  testProject,
  Routes,
} from "@/fixtures";
import { user } from "@/fixtures/data/user";
describe("Bulk Project Creation", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects();
  });

  beforeEach(() => {
    cy.viewport(1920, 1080);
    cy.loginToPage(
      user.validUser.email,
      user.validUser.password,
      Routes.PROJECT_CREATOR,
      { tab: "bulk" }
    );
  });

  describe("I cannot create a project without a name", () => {
    it("Cant create a project without a name", () => {
      cy.inputText(
        DataCy.creationBulkDescriptionInput,
        testProject.name
      ).uploadFiles(DataCy.creationBulkFilesInput, simpleProjectFilesMap.tim);

      cy.getCy(DataCy.creationUploadButton).should("be.disabled");
    });
  });

  describe("I can create an empty project", () => {
    it("Can create an empty project on the bulk upload tab", () => {
      cy.setProjectIdentifier("bulk");

      cy.getCy(DataCy.creationUploadButton).should("be.disabled");

      cy.clickButton(DataCy.creationEmptyToggle).clickButton(
        DataCy.creationUploadButton
      );

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });

    it("Can create an empty project in the project selector", () => {
      cy.openProjectSelector().clickButton(DataCy.selectorAddButton);

      cy.setProjectIdentifier("modal")
        .clickButton(DataCy.creationEmptyToggle)
        .clickButton(DataCy.creationUploadButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
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
