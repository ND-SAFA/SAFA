import {
  validUser,
  simpleProjectFiles,
  simpleProjectFilesMap,
  DataCy,
} from "../fixtures";
import { testProject } from "../fixtures/project";

describe("Project Creation", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080/create").login(
      validUser.email,
      validUser.password
    );
  });

  describe("I can create a project from files uploaded in bulk", () => {
    beforeEach(() => {
      cy.switchTab("Bulk Upload");
    });

    it("cant create a project without a name", () => {
      cy.getCy(DataCy.creationBulkDescriptionInput).type(testProject.name);
      cy.uploadFiles(DataCy.creationBulkFilesInput, simpleProjectFilesMap.tim);

      cy.getCy(DataCy.creationUploadButton).should("be.disabled");
    });

    it("cant create a project without any files", () => {
      cy.getCy(DataCy.creationBulkNameInput).type(testProject.name);
      cy.getCy(DataCy.creationBulkDescriptionInput).type(
        testProject.description
      );

      cy.getCy(DataCy.creationUploadButton).should("be.disabled");
    });

    it("can create a valid project", () => {
      cy.getCy(DataCy.creationBulkNameInput).type(testProject.name);
      cy.getCy(DataCy.creationBulkDescriptionInput).type(
        testProject.description
      );
      cy.uploadFiles(DataCy.creationBulkFilesInput, ...simpleProjectFiles);

      cy.getCy(DataCy.creationUploadButton).should("not.be.disabled").click();

      cy.getCy(DataCy.jobStatus, "first", 5000)
        .wait(5000)
        .should("contain.text", "Completed");

      cy.clickButton(DataCy.jobPanel).clickButton(DataCy.jobDeleteButton);
    });
  });
});
