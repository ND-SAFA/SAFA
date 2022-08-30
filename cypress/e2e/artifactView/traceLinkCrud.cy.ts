import { DataCy, validUser } from "../../fixtures";

describe("Trace Link CRUD", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects();

    cy.visit("/create")
      .login(validUser.email, validUser.password)
      .location("pathname", { timeout: 5000 })
      .should("equal", "/create");

    cy.createBulkProject()
      .getCy(DataCy.jobStatus, "first")
      .should("contain.text", "Completed");

    cy.logout();
  });

  beforeEach(() => {
    cy.visit("/project")
      .login(validUser.email, validUser.password)
      .location("pathname", { timeout: 5000 })
      .should("equal", "/project");

    cy.getNodes().should("be.visible");
  });

  describe("I can create a new trace link", () => {
    it("Cannot create restricted links", () => {
      // Selects two of the same artifact.
      cy.createNewTraceLink()
        .getCy(DataCy.traceSaveSubmitButton)
        .should("be.disabled");

      // Selects an existing link.
      cy.fillTraceLinkModal("F15", "F9")
        .getCy(DataCy.traceSaveSubmitButton)
        .should("be.disabled");

      // Selects an invalid link direction.
      cy.fillTraceLinkModal("F5", "D3")
        .getCy(DataCy.traceSaveSubmitButton)
        .should("be.disabled");
    });

    it("Creates a new trace link from the modal", () => {
      cy.createNewTraceLink("D3", "F5").saveTraceLink();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });

    // it("Draws a new trace link");
  });

  describe("I can delete a trace link", () => {
    it("Deletes a trace link", () => {
      cy.createNewArtifact({ parent: "{downArrow}{enter}" }).saveArtifact();

      cy.getCy(DataCy.selectedPanelParents).should("be.visible").click();
      cy.getCy(DataCy.selectedPanelParentItem)
        .first()
        .within(() => {
          cy.clickButton(DataCy.selectedPanelParentLinkButton);
        });

      cy.getCy(DataCy.traceApproveModal).within(() => {
        cy.clickButton(DataCy.traceDeleteButton).clickButton(
          DataCy.traceDeleteButton
        );
      });

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.selectedPanelParents).should("not.exist");
    });
  });
});
