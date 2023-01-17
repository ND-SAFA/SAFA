import { before } from "mocha";
import { DataCy } from "../../fixtures";
import { validUser } from "../../fixtures/data/user.json";

describe("Project Commits", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects();

    cy.visit("/create")
      .login(validUser.email, validUser.password)
      .location("pathname", { timeout: 2000 })
      .should("equal", "/create");

    cy.createBulkProject()
      .waitForJobLoad()
      .clickButton(DataCy.jobOpenButton)
      .openApproveGeneratedTraceLinks()
      .clickButton(DataCy.sidebarCloseButton);
  });

  describe("Project Commit Changes", () => {
    beforeEach(() => {
      cy.viewport(1024, 768);
      cy.dbResetVersions();

      cy.visit("/login")
        .login(validUser.email, validUser.password)
        .location("pathname", { timeout: 2000 })
        .should("equal", "/");

      cy.getCy(DataCy.navOpenProjectButton).click();
      cy.withinTableRows(DataCy.selectionProjectList, (tr) => {
        tr.should("have.length", 2);
        tr.last().click();
      });

      // Create a new version of the project
      cy.getCy(DataCy.selectorAddButton).should("be.visible").last().click();
      cy.getCy(DataCy.versionCreateMinorButton).click();

      cy.withinTableRows(DataCy.selectionVersionList, (tr) => {
        tr.should("have.length", 3); // This will wait until the table populates
        tr.contains("2").click();
      });

      cy.getCy(DataCy.artifactTree).should("be.visible");
    });

    describe("I can create a commit to create an artifact", () => {
      it("Creates a commit to create an artifact", () => {
        // Verify that the undo button is disabled
        cy.getCy(DataCy.navUndoButton).should("have.class", "disable-events");

        // Create a New Artifact + Verify it exists
        cy.createNewArtifact({
          name: "Test Commit Artifact",
          type: "Designs",
          body: "Test Commit Artifact Body",
          parent: "N/A",
        }).saveArtifact();

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        cy.getCy(DataCy.selectedPanelCloseButton).click();

        cy.getNode("Test Commit Artifact")
          .should("be.visible")
          .should("have.length", 1);

        // Verify that the undo button is enabled
        cy.getCy(DataCy.navUndoButton).should(
          "not.have.class",
          "disable-events"
        );
      });
    });

    describe("I can undo a committed change", () => {
      it("Resets and updates artifacts when undone", () => {
        // Create a new artifact
        cy.createNewArtifact({
          name: "Test Undo Artifact",
          type: "Designs",
          body: "Test Undo Artifact Body",
          parent: "N/A",
        }).saveArtifact();

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        cy.getCy(DataCy.selectedPanelCloseButton).click();
        cy.reload();
        cy.getCy(DataCy.treeNode).should("be.visible");

        // Edit the new artifact body
        cy.getNode("Test Undo Artifact").click();
        cy.getCy(DataCy.selectedPanelEditButton).click();
        cy.getCy(DataCy.artifactSaveBodyInput).clear();
        cy.inputText(DataCy.artifactSaveBodyInput, "Changed!");
        cy.getCy(DataCy.artifactSaveSubmitButton).click();

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        cy.getCy(DataCy.selectedPanelCloseButton).click();

        //Check that undo button is enabled
        cy.getCy(DataCy.navUndoButton).should("not.be.disabled");

        //Undo the change
        cy.getCy(DataCy.navUndoButton).click();
        cy.getCy(DataCy.snackbarUpdate).should("be.visible");

        // Check that the edit was undone
        cy.getNode("Test Undo Artifact").should(
          "contain.text",
          "Test Undo Artifact Body"
        );
        cy.getCy(DataCy.navUndoButton).should("have.class", "disable-events");
      });

      it("Removes a committed artifact when undone", () => {
        // Create an artifact
        cy.getCy(DataCy.navUndoButton).should("have.class", "disable-events");
        cy.createNewArtifact({
          name: "Test Commit Artifact New Commit",
          type: "Designs",
          body: "Test Commit Artifact Body",
          parent: "N/A",
        }).saveArtifact();
        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        cy.getCy(DataCy.selectedPanelBody).should("be.visible");
        cy.getCy(DataCy.selectedPanelCloseButton).click();
        cy.getNode("Test Commit Artifact New Commit").should("be.visible");

        // Undo
        cy.getCy(DataCy.navUndoButton).click();
        cy.getCy(DataCy.snackbarUpdate).should("be.visible");

        // Check that it's not visible
        cy.getNode("Test Commit Artifact New Commit").should("not.exist");
      });

      it.skip("Resets an updated trace link when undone", () => {
        // Navigate to the trace link table
        cy.getCy(DataCy.navTraceLinkApprovalButton).click();
        cy.clickButtonWithName("Trace Approval");

        // Approve the first trace link (Should be "D10" be default)
        cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
          tr.should("have.length.at.least", 2)
            .first()
            .clickButton(DataCy.traceApproveButton);
        });

        // Undo the change
        cy.getCy(DataCy.navArtifactViewButton).click();
        cy.getCy(DataCy.treeNode).should("be.visible");
        cy.getCy(DataCy.navUndoButton)
          .should("not.have.class", "disable-events")
          .click();

        cy.getCy(DataCy.snackbarUpdate).should("be.visible");

        // Check that the trace link is not approved on the table or tree
        cy.getCy(DataCy.navTraceLinkApprovalButton).click();
        cy.clickButtonWithName("Trace Approval");
        cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
          tr.should("have.length.at.least", 2).should("contain.text", "D10");
        });
      });

      it.skip("Restores deleted trace links on a deleted artifact when undone", () => {
        cy.on("uncaught:exception", () => false);

        // Delete an artifact with a trace link
        cy.getNode("D5").click();
        cy.getCy(DataCy.selectedPanelDeleteButton).click();
        cy.getCy(DataCy.confirmModalButton).click();
        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        cy.getCy(DataCy.snackbarCloseButton).click();

        // Undo the change
        cy.getCy(DataCy.navUndoButton)
          .should("not.have.class", "disable-events")
          .click();

        // Check that the trace link is visible on the table and tree (See side link panel)
        cy.getNode("F6").click();
        cy.getCy(DataCy.selectedPanelChildItem)
          .should("have.length", 6)
          .and("contain.text", "D5");
      });
    });

    describe("I can redo a committed change", () => {
      it("Adds a committed artifact when redone", () => {
        //Create an artifact
        cy.getCy(DataCy.navUndoButton).should("have.class", "disable-events");
        cy.createNewArtifact({
          name: "Test Commit Artifact Redo",
          type: "Designs",
          body: "Test Commit Artifact Body",
          parent: "N/A",
        }).saveArtifact();
        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        cy.getCy(DataCy.selectedPanelBody).should("be.visible");
        cy.getCy(DataCy.selectedPanelCloseButton).click();
        cy.getNode("Test Commit Artifact Redo").should("be.visible");

        // Undo
        cy.getCy(DataCy.navUndoButton).click();

        // Check that its not visible
        cy.getNode("Test Commit Artifact Redo").should("not.exist");

        // Redo
        cy.getCy(DataCy.navRedoButton).click();

        // Check that its visible again
        cy.getNode("Test Commit Artifact Redo").should("be.visible");
        cy.getCy(DataCy.navUndoButton).should(
          "not.have.class",
          "disable-events"
        );
      });
    });
  });
});
