import { DataCy, Routes, simpleProjectFiles } from "@/fixtures";

describe("Project Versions", () => {
  beforeEach(() => {
    cy.initEmptyProject();

    cy.expandViewport()
      .visit(Routes.MY_PROJECTS)
      .locationShouldEqual(Routes.MY_PROJECTS);
  });

  describe("I can create a new major, minor, or revision version", () => {
    it("Can create a new major version", () => {
      cy.projectSelectorContinue("project").createNewVersion("major");

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });

    it("Can create a new minor version", () => {
      cy.projectSelectorContinue("project").createNewVersion("minor");

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });

    it("Can create a new revision version", () => {
      cy.projectSelectorContinue("project").createNewVersion("revision");

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("I can delete a project version", () => {
    it("Deletes a version", () => {
      cy.projectSelectorContinue("project").createNewVersion("revision");

      cy.getCy(DataCy.selectionVersionList).within(() => {
        cy.clickButton(DataCy.selectorDeleteButton);
      });

      cy.clickButton(DataCy.confirmModalButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("I can upload new flat files to a project version", () => {
    it("Uploads files to the current version", () => {
      cy.projectSelectorContinue("project")
        .projectSelectorContinue("version")
        .openUploadFiles();

      cy.uploadFiles(
        DataCy.versionUploadFilesInput,
        ...simpleProjectFiles
      ).clickButton(DataCy.versionUploadFilesButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });
});
