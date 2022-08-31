import { DataCy, DataIds, validUser } from "../../fixtures";

describe("Artifact CRUD", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects();

    cy.visit("/create")
      .login(validUser.email, validUser.password)
      .location("pathname", { timeout: 5000 })
      .should("equal", "/create");

    cy.createBulkProject()
      .getCy(DataCy.jobStatus, "first", 20000)
      .should("contain.text", "Completed");

    cy.logout();
  });

  beforeEach(() => {
    cy.visit("/project")
      .login(validUser.email, validUser.password)
      .location("pathname", { timeout: 5000 })
      .should("equal", "/project");

    cy.getCy(DataCy.appLoading)
      .should("not.be.visible")
      .getNodes()
      .should("be.visible");
  });

  describe("I can create a new artifact", () => {
    it("Cannot create an artifact without a name, type, or body", () => {
      cy.createNewArtifact({ name: "" });

      cy.getCy(DataCy.artifactSaveModal).within(() => {
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
    });

    it("Cannot create a new artifact with the same name", () => {
      const name = `New ${Math.random()}`;

      cy.createNewArtifact({ name }).saveArtifact();

      cy.createNewArtifact({ name });

      cy.getCy(DataCy.artifactSaveModal).within(() => {
        cy.contains("Name is already used");
        cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");
      });
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
      cy.get("canvas")
        .first()
        .then(($el) =>
          cy.wrap($el).rightclick($el.width() / 4, $el.height() / 4)
        );

      // Click the add artifact button.
      cy.get(DataIds.rightClickAddArtifact)
        .should("be.visible")
        .then(($el) => $el.click());

      cy.fillArtifactModal({ name }).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain", name);
    });

    it("Creates an artifact with a new type", () => {
      const name = `New ${Math.random()}`;

      cy.createNewArtifact({ name, type: "New Type{enter}" });

      cy.getCy(DataCy.artifactSaveModal).within(() => {
        cy.clickButton(DataCy.artifactSaveSubmitButton);
      });

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain", name);
    });

    it("Adds an artifact as a child of another artifact", () => {
      cy.createNewArtifact({ parent: "{downArrow}{enter}" }).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("be.visible");

      cy.getCy(DataCy.selectedPanelParents).should("be.visible").click();
      cy.getCy(DataCy.selectedPanelParentItem)
        .should("be.visible")
        .should("have.length", 1);
    });
  });

  describe("I can delete an artifact", () => {
    it("Deletes a new artifact", () => {
      cy.createNewArtifact({}).saveArtifact();

      cy.getCy(DataCy.selectedPanelDeleteButton).click();
      cy.getCy(DataCy.confirmModalButton).click();

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

      cy.getCy(DataCy.artifactSaveModal).within(() => {
        cy.getCy(DataCy.artifactSaveNameInput)
          .should("have.value", name)
          .clear();

        cy.inputText(DataCy.artifactSaveNameInput, editedName);
        cy.clickButton(DataCy.artifactSaveSubmitButton);
      });

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain.text", editedName);
    });
  });

  describe("I can duplicate an artifact", () => {
    it("Duplicates an artifact in view", () => {
      // Wait for graph to center.
      cy.clickButton(DataCy.navGraphCenterButton).wait(200);

      // Right click on a visible node.
      cy.getNodes().should("be.visible").first().rightclick();

      cy.get(DataIds.rightClickDuplicateArtifact)
        .should("be.visible")
        .then(($el) => $el.click());

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain.text", "(Copy)");
    });
  });
});
