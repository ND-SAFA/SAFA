import { DataCy } from "../../fixtures";

describe("Document CRUD", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject()
      .openDocumentSelector()
      .clickButton(DataCy.documentItemButton, "last")
      .getCy(DataCy.appLoading)
      .should("not.be.visible");
  });

  describe("I can create a new document from artifacts or their types", () => {
    it("Cant create a document without a name", () => {
      cy.createDocument({ name: "" });

      cy.getCy(DataCy.documentSaveButton).should("be.disabled");
    });

    it("Cant create a document with an existing name", () => {
      const name = "New Document";

      // Create a new document.
      cy.createDocument({ name, artifacts: "F5{downArrow}{enter}" })
        .saveDocument()
        .getCy(DataCy.snackbarSuccess)
        .should("be.visible");

      // Assert that the document cant be named default.
      cy.createDocument({ name: "Default" })
        .getCy(DataCy.documentSaveButton)
        .should("be.disabled");

      // Assert that the document cannot have the same name as another.
      cy.getCy(DataCy.documentNameInput)
        .clear()
        .inputText(DataCy.documentNameInput, name)
        .getCy(DataCy.documentSaveButton)
        .should("be.disabled");
    });

    it("Creates a document from artifacts", () => {
      cy.createDocument({
        artifacts: "{downArrow}{enter}{downArrow}{enter}",
      }).saveDocument();

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .getCy(DataCy.documentModal)
        .should("not.be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length", 2);
    });

    it("Creates a document from artifact types", () => {
      cy.createDocument({
        includeTypes: "Req{downArrow}{enter}",
      }).saveDocument();

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .getCy(DataCy.documentModal)
        .should("not.be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length", 5);
    });
  });

  describe("I can create a document from a parent artifact and a list of child artifact types", () => {
    it("Creates a document with the tree of a parent", () => {
      cy.createDocument({
        artifacts: "F5{downArrow}{enter}",
        includeChildTypes: "Des{downArrow}{enter}",
      }).saveDocument();

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .getCy(DataCy.documentModal)
        .should("not.be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length", 3);
    });
  });

  describe("I can create a table document", () => {
    it("Creates a document and shows the table", () => {
      cy.createDocument({
        type: "FMEA",
        includeTypes: "Req{downArrow}{enter}",
      }).saveDocument();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.artifactTable).should("be.visible");
    });
  });

  describe("I can edit a document", () => {
    it("Adds new artifacts to a document", () => {
      cy.createDocument({
        artifacts: "F5{downArrow}{enter}",
      }).saveDocument();

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .getCy(DataCy.documentModal)
        .should("not.be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length", 1);

      cy.openDocumentEditor()
        .fillDocumentFields({
          includeChildTypes: "Des{downArrow}{enter}",
        })
        .saveDocument();

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .getCy(DataCy.documentModal)
        .should("not.be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length", 3);
    });
  });

  describe("I can delete a document", () => {
    it("Deletes a document", () => {
      cy.createDocument({
        artifacts: "F5{downArrow}{enter}",
      }).saveDocument();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getNodes().should("have.length", 1);

      cy.openDocumentEditor()
        .getCy(DataCy.documentModal)
        .within(() => {
          cy.clickButton(DataCy.documentDeleteButton).clickButton(
            DataCy.documentDeleteButton
          );
        });

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .getCy(DataCy.documentModal)
        .should("not.be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length.above", 1);
    });
  });

  describe("I can switch between project documents", () => {
    it("Switches to a new document, then back to the default", () => {
      cy.createDocument({
        artifacts: "F5{downArrow}{enter}",
      }).saveDocument();

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .getCy(DataCy.documentModal)
        .should("not.be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length", 1);

      cy.openDocumentSelector().clickButtonWithName("Default");

      cy.getCy(DataCy.documentModal)
        .should("not.be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length.above", 1);
    });
  });
});
