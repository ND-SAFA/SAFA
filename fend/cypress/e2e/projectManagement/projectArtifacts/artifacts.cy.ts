import { DataCy } from "@/fixtures";

describe("Artifacts", () => {
  before(() => {
    cy.initEmptyProject();
  });

  beforeEach(() => {
    cy.initProjectVersion(false);
  });

  describe("I can create a new artifact", () => {
    it("Cannot create an artifact without a name, type, or body", () => {
      cy.createNewArtifact({ name: "" });

      cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");

      cy.inputText(DataCy.artifactSaveNameInput, `New ${Math.random()}`);
      cy.inputText(DataCy.artifactSaveBodyInput, "", true);

      cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");

      cy.inputText(DataCy.artifactSaveBodyInput, "New Artifact");
      cy.inputText(DataCy.artifactSaveTypeInput, "{backspace}");

      cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");

      cy.inputText(DataCy.artifactSaveTypeInput, "Design{downArrow}{enter}");

      cy.getCy(DataCy.artifactSaveSubmitButton).should("be.enabled");
    });

    it("Creates a simple new artifact", () => {
      const name = `New ${Math.random()}`;

      cy.createNewArtifact({ name }, true);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain", name);
    });

    it.skip("Cannot create a new artifact with the same name", () => {
      const name = `New ${Math.random()}`;

      cy.createNewArtifact({ name }, true, true).createNewArtifact({ name });

      cy.contains("This name is already used, please select another.");
      cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");
    });

    it("Creates a new artifact from the right click menu", () => {
      const name = `New ${Math.random()}`;

      cy.get("canvas")
        .first()
        .then(($el) =>
          cy.wrap($el).rightclick($el.width() / 2, $el.height() / 2)
        );

      cy.getCy(DataCy.rightClickAddArtifact)
        .should("be.visible")
        .then(($el) => $el.click());

      cy.fillArtifactFields({ name }).clickButton(
        DataCy.artifactSaveSubmitButton
      );

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain", name);
    });

    it("Adds an artifact as a child of another artifact", () => {
      cy.createNewArtifact({}, true, true).createNewArtifact(
        { parent: "{downArrow}{enter}" },
        true
      );

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
      cy.createNewArtifact({}, true);

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

      cy.createNewArtifact({ name }, true);

      cy.clickButton(DataCy.selectedPanelEditButton);

      cy.getCy(DataCy.artifactSaveNameInput).should("have.value", name).clear();

      cy.inputText(DataCy.artifactSaveNameInput, editedName);
      cy.clickButton(DataCy.artifactSaveSubmitButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain.text", editedName);
    });
  });
});
