import { DataCy } from "../../fixtures";
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
      const name = "Test Artifact";

      cy.createNewArtifact({
        name,
      }).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.getCy(DataCy.artifactTableArtifact).contains(name).should("exist");
    });
  });

  describe("I can edit a row of the artifact table", () => {
    it("Edits an artifact in the table", () => {
      const name = `Test Artifact Edit`;
      const newBody = "(Edited Body Content)";

      cy.createNewArtifact({
        name,
      }).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.getCy(DataCy.artifactTableArtifact)
        .contains(name)
        .click()
        .parent()
        .parent()
        .parent()
        .within(() => {
          cy.getCy(DataCy.artifactTableEditArtifactRowButton).click();
        });

      cy.inputText(DataCy.artifactSaveBodyInput, newBody).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.getCy(DataCy.selectedPanelBody).contains(newBody).should("exist");
    });
  });

  describe("I can delete a row of the artifact table", () => {
    it("Deletes the test artifact in the table", () => {
      const name = `Test Artifact Delete`;

      cy.createNewArtifact({
        name,
      }).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.getCy(DataCy.artifactTableArtifact)
        .contains(name)
        .click()
        .parent()
        .parent()
        .parent()
        .within(() => {
          cy.getCy(DataCy.artifactTableDeleteArtifactRowButton).click();
        });

      cy.clickButton(DataCy.confirmModalButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.getCy(DataCy.artifactTableArtifact).contains(name).should("not.exist");
    });
  });

  describe("I can see missing required fields in each row", () => {
    //TODO: Add tests for seeing missing required fields in each row
  });
});
