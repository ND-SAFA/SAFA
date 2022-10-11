import {
  validUser,
  simpleProjectFiles,
  simpleProjectFilesMap,
  DataCy,
  testProject,
} from "../../fixtures";

describe("Project Creation", () => {
  beforeEach(() => {
    cy.dbResetJobs();
    cy.dbResetProjects();

    cy.visit("/create?tab=bulk").login(validUser.email, validUser.password);

    cy.location("pathname", { timeout: 2000 }).should("equal", "/create");
  });

  describe("I can create a project from files uploaded in bulk", () => {
    it("cant create a project without a name", () => {
      cy.getCy(DataCy.creationBulkDescriptionInput).type(testProject.name);
      cy.uploadFiles(DataCy.creationBulkFilesInput, simpleProjectFilesMap.tim);

      cy.getCy(DataCy.creationUploadButton).should("be.disabled");
    });

    it("cant create a project without any files", () => {
      cy.setProjectIdentifier("bulk");

      cy.getCy(DataCy.creationUploadButton).should("be.disabled");
    });

    it("can create a valid project", () => {
      cy.setProjectIdentifier("bulk");
      cy.uploadFiles(DataCy.creationBulkFilesInput, ...simpleProjectFiles);

      cy.getCy(DataCy.creationUploadButton).should("not.be.disabled").click();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });
});
