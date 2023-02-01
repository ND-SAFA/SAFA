import {
  validUser,
  simpleProjectFiles,
  simpleProjectFilesMap,
  DataCy,
  testProject,
  Routes,
} from "@/fixtures";

describe("Bulk Project Creation", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects();
  });

  beforeEach(() => {
    cy.visit(Routes.PROJECT_CREATOR + "?tab=bulk")
      .login(validUser.email, validUser.password)
      .locationShouldEqual(Routes.PROJECT_CREATOR);
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

      cy.getCy(DataCy.projectEditModal).within(() => {
        cy.setProjectIdentifier("modal")
          .clickButton(DataCy.creationEmptyToggle)
          .clickButton(DataCy.creationUploadButton);
      });

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
