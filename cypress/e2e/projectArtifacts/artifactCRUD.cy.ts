import { DataCy, DataIds } from "../../fixtures";

describe("Artifact CRUD", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
  });

  describe("I can create a new artifact", () => {
    it("Cannot create an artifact without a name, type, or body", () => {
      cy.createNewArtifact({ name: "" });

      cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");

      cy.inputText(DataCy.artifactSaveNameInput, `New ${Math.random()}`);
      cy.getCy(DataCy.artifactSaveBodyInput).clear();

      cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");

      cy.inputText(DataCy.artifactSaveBodyInput, "New Artifact");
      cy.getCy(DataCy.artifactSaveTypeInput).clear();

      cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");

      cy.inputText(DataCy.artifactSaveTypeInput, "Designs{downArrow}{enter}");

      cy.getCy(DataCy.artifactSaveSubmitButton).should("be.enabled");
    });

    it("Cannot create a new artifact with the same name", () => {
      const name = `New ${Math.random()}`;

      cy.createNewArtifact({ name }).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .clickButton(DataCy.selectedPanelCloseButton);

      cy.createNewArtifact({ name });

      cy.contains("This name is already used, please select another.");
      cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");
    });

    it("Creates a simple new artifact", () => {
      const name = `New ${Math.random()}`;

      cy.createNewArtifact({ name }).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain", name);
    });

    it("Creates a new artifact from the right click menu", () => {
      const name = `New ${Math.random()}`;

      // Opens the right click window.
      // cy.get("canvas")
      //   .first()
      //   .then(($el) =>
      //     cy.wrap($el).rightclick($el.width() / 2, $el.height() / 2)
      //   );

      cy.centerGraph().getNodes().first().rightclick();

      // Click the add artifact button.
      cy.get(DataIds.rightClickAddArtifact)
        .should("be.visible")
        .then(($el) => $el.click());

      cy.fillArtifactModal({ name }).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain", name);
    });

    it("Adds an artifact as a child of another artifact", () => {
      cy.createNewArtifact({ parent: "{downArrow}{enter}" }).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("be.visible");

      cy.getCy(DataCy.selectedPanelParents).should("be.visible");
      cy.getCy(DataCy.selectedPanelParentItem)
        .should("be.visible")
        .should("have.length", 1);
    });
  });

  describe("I can delete an artifact", () => {
    it("Deletes a new artifact", () => {
      cy.createNewArtifact({}).saveArtifact();

      cy.clickButton(DataCy.selectedPanelDeleteButton).clickButton(
        DataCy.confirmModalButton
      );

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("not.exist");
      cy.getNodes(true).should("not.exist");
    });
  });

  describe("I can edit an artifact", () => {
    it("Edits an artifact's name", () => {
      const name = `New ${Math.random()}`;
      const editedName = `New ${Math.random()}`;

      cy.createNewArtifact({ name }).saveArtifact();

      cy.getCy(DataCy.selectedPanelEditButton).click();

      cy.getCy(DataCy.artifactSaveNameInput).should("have.value", name).clear();

      cy.inputText(DataCy.artifactSaveNameInput, editedName);
      cy.clickButton(DataCy.artifactSaveSubmitButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain.text", editedName);
    });
  });

  describe("I can duplicate an artifact", () => {
    it("Duplicates an artifact in view", () => {
      cy.centerGraph();

      // Open the right click menu on a visible node.
      cy.getNodes().should("be.visible").first().rightclick();

      cy.get(DataIds.rightClickDuplicateArtifact)
        .should("be.visible")
        .then(($el) => $el.click());

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain.text", "(Copy)");
    });
  });
});
