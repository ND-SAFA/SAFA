import { DataCy } from "@/fixtures";

describe("Documents", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.dbResetDocuments().initProjectVersion().expandViewport();
  });

  describe("I can create a new document from artifacts or their types", () => {
    it("Cant create a document without a name", () => {
      cy.createDocument({ name: "" });

      cy.getCy(DataCy.documentSaveButton).should("be.disabled");
    });

    it("Cant create a document with an existing name", () => {
      const name = "New Document";

      // Create a new document.
      cy.createDocument({ name, artifacts: "F5{downArrow}{enter}" }, true)
        .getCy(DataCy.snackbarSuccess)
        .should("be.visible");

      // Assert that the document cant be named default.
      cy.createDocument({ name: "All Artifacts" })
        .getCy(DataCy.documentSaveButton)
        .should("be.disabled");

      // Assert that the document cannot have the same name as another.
      cy.inputText(DataCy.documentNameInput, name, true)
        .getCy(DataCy.documentSaveButton)
        .should("be.disabled");
    });

    it("Creates a document from artifacts", () => {
      cy.createDocument(
        {
          artifacts: "{downArrow}{enter}{downArrow}{enter}",
        },
        true
      );

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length", 2);
    });

    it("Creates a document from artifact types", () => {
      cy.createDocument(
        {
          includeTypes: "Req{downArrow}{enter}",
        },
        true
      );

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length", 5);
    });
  });

  describe("I can create a document from a parent artifact and a list of child artifact types", () => {
    it("Creates a document with the tree of a parent", () => {
      cy.createDocument(
        {
          artifacts: "F5{downArrow}{enter}",
          includeChildTypes: "Des{downArrow}{enter}",
        },
        true
      );

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length", 3);
    });
  });

  describe("I can edit a document", () => {
    it("Adds new artifacts to a document", () => {
      const name = `New ${Math.random()}`;

      cy.createDocument(
        {
          name,
          artifacts: "F5{downArrow}{enter}",
        },
        true
      );

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length", 1);

      cy.openDocumentEditor(name)
        .fillDocumentFields({
          includeChildTypes: "Des{downArrow}{enter}",
        })
        .clickButton(DataCy.documentSaveButton);

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length", 3);
    });
  });

  describe("I can delete a document", () => {
    it("Deletes a document", () => {
      const name = `New ${Math.random()}`;

      cy.createDocument(
        {
          name,
          artifacts: "F5{downArrow}{enter}",
        },
        true
      );

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getNodes().should("have.length", 1);

      cy.openDocumentEditor(name)
        .clickButton(DataCy.documentDeleteButton)
        .clickButton(DataCy.confirmModalButton);

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length.above", 1);
    });
  });

  describe("I can switch between project documents", () => {
    it("Switches to a new document, then back to the default", () => {
      cy.createDocument(
        {
          artifacts: "F5{downArrow}{enter}",
        },
        true
      );

      cy.getCy(DataCy.snackbarSuccess)
        .should("be.visible")
        .waitForProjectLoad();
      cy.getNodes().should("have.length", 1);

      cy.openDocumentSelector().clickButtonWithName("All Artifacts");

      cy.waitForProjectLoad();
      cy.getNodes().should("have.length.above", 1);
    });
  });
});
