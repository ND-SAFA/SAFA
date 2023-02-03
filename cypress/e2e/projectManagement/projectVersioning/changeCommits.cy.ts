import { DataCy } from "@/fixtures";

describe("Change Commits", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion();
  });

  describe("I can create a commit to change project entities", () => {
    it("Commits an artifact", () => {
      const name = "Test Commit Artifact";

      cy.getCy(DataCy.navUndoButton).should("have.class", "disable-events");

      cy.createNewArtifact({ name }, true, true);

      cy.getNode(name).should("be.visible");
      cy.getCy(DataCy.navUndoButton).should("not.have.class", "disable-events");
    });
  });

  describe("I can undo a committed change", () => {
    it("Undoes a created artifact", () => {
      const name = "Test Undo Artifact";

      cy.createNewArtifact({ name }, true, true);

      cy.getNode(name).should("be.visible");
      cy.getCy(DataCy.navUndoButton).should("not.have.class", "disable-events");

      cy.clickButton(DataCy.navUndoButton);

      cy.getCy(DataCy.snackbarUpdate).should("be.visible");
      cy.getNode(name).should("not.exist");
      cy.getCy(DataCy.navUndoButton).should("have.class", "disable-events");
    });

    it("Undoes edits to an artifact", () => {
      const name = "Test Undo Artifact";
      const changedName = "Test Changed Artifact";

      cy.createNewArtifact({ name }, true, true);
      cy.clickButton(DataCy.snackbarCloseButton);

      cy.centerGraph()
        .getNode(name)
        .click()
        .clickButton(DataCy.selectedPanelEditButton);

      cy.getCy(DataCy.artifactSaveNameInput)
        .clear()
        .inputText(DataCy.artifactSaveNameInput, changedName)
        .clickButton(DataCy.artifactSaveSubmitButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.clickButton(DataCy.selectedPanelCloseButton);

      cy.getCy(DataCy.navUndoButton).should("not.have.class", "disable-events");

      cy.clickButton(DataCy.navUndoButton);

      cy.getCy(DataCy.snackbarUpdate).should("be.visible");
      cy.getNode(name).should("be.visible");
    });

    it.skip("Undoes changes to a trace link", () => {
      cy.openApproveGeneratedTraceLinks();

      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.filter(":visible").should("have.length", 10);
        tr.clickButton(DataCy.traceApproveButton, "first");
      });

      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.filter(":visible").should("have.length", 9);
      });

      cy.getCy(DataCy.navUndoButton).should("not.have.class", "disable-events");

      cy.clickButton(DataCy.navUndoButton);

      cy.getCy(DataCy.snackbarUpdate).should("be.visible");

      cy.withinTableRows(DataCy.traceLinkTable, (tr) => {
        tr.filter(":visible").should("have.length", 10);
      });
    });

    it.skip("Restores deleted trace links on a deleted artifact", () => {
      cy.on("uncaught:exception", () => false);

      const existingName = "D5";
      const parentName = "F6";

      cy.getNode(existingName).click();

      cy.clickButton(DataCy.selectedPanelDeleteButton).clickButton(
        DataCy.confirmModalButton
      );

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getNode(existingName).should("not.exist");
      cy.getCy(DataCy.navUndoButton).should("not.have.class", "disable-events");

      cy.clickButton(DataCy.navUndoButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.centerGraph().getNode(parentName).click();
      cy.getCy(DataCy.selectedPanelChildItem)
        .should("have.length", 6)
        .and("contain.text", existingName);
    });
  });

  describe("I can redo a committed change", () => {
    it("Reverts a deleted artifact", () => {
      const name = "Test Redo Artifact";

      cy.createNewArtifact({ name }, true, true);

      cy.getNode(name).should("be.visible");

      cy.clickButton(DataCy.navUndoButton);

      cy.getCy(DataCy.snackbarUpdate).should("be.visible");
      cy.getNode(name).should("not.exist");
      cy.getCy(DataCy.navRedoButton).should("not.have.class", "disable-events");

      cy.clickButton(DataCy.navRedoButton);

      cy.getCy(DataCy.snackbarUpdate).should("be.visible");
      cy.getNode(name).should("be.visible");
      cy.getCy(DataCy.navRedoButton).should("have.class", "disable-events");
    });
  });
});
