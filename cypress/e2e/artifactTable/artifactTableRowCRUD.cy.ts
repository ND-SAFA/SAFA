import { DataCy, validUser } from "../../fixtures";
import "cypress-wait-until";

describe("Artifact Table Row CRUD", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
    cy.switchToTableView();
  });

  describe("I can add a row to the artifact table", () => {
    it("Adds an artifact to the table", () => {
      cy.clickButton(DataCy.artifactTableAddContentButton);
      cy.clickButton(DataCy.artifactTableAddArtifactButton);
      cy.addTableArtifact(
        "Test Artifact",
        "Test Type",
        "default",
        "default",
        "Test Body",
        "Test Summary"
      );
      cy.waitUntil(function () {
        return cy
          .getCy(DataCy.artifactTableCreateArtifactSaveButton)
          .should("not.be.visible");
      });
      cy.getCy(DataCy.artifactTableArtifact)
        .last()
        .contains("Test Artifact")
        .should("exist");
    });
  });

  describe("I can edit a row of the artifact table", () => {
    it("Edits the test artifact in the table", () => {
      cy.getCy(DataCy.artifactTableArtifact)
        .last()
        .contains("Test Artifact")
        .should("exist");
      cy.getCy(DataCy.artifactTableEditArtifactRowButton).last().click();
      cy.inputText(
        DataCy.artifactTableCreateArtifactBodyInput,
        " (Edited Body Content)"
      );
      cy.clickButton(DataCy.artifactTableCreateArtifactSaveButton);
      cy.waitUntil(function () {
        return cy
          .getCy(DataCy.artifactTableCreateArtifactSaveButton)
          .should("not.be.visible");
      });
      cy.getCy(DataCy.artifactTableArtifactPanelBody)
        .contains("Test Body (Edited Body Content")
        .should("exist");
    });
  });

  describe("I can delete a row of the artifact table", () => {
    it("Deletes the test artifact in the table", () => {
      cy.getCy(DataCy.artifactTableArtifact)
        .last()
        .contains("Test Artifact")
        .should("exist");
      cy.getCy(DataCy.artifactTableDeleteArtifactRowButton).last().click();
      cy.clickButton(DataCy.confirmModalButton);
      cy.getCy(DataCy.artifactTableArtifact)
        .last()
        .contains("Test Artifact")
        .should("not.exist");
    });
  });

  describe("I can see missing required fields in each row", () => {
    //TODO: Add tests for seeing missing required fields in each row
  });
});
