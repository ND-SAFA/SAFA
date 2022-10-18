import { DataCy } from "../../fixtures";

describe("Trace Link CRUD", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
  });

  describe("I can create a new trace link", () => {
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

  describe("Trace Link Direction Rules", () => {
    describe("I cannot create trace links between types in both directions", () => {
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
        cy.fillTraceLinkModal("F5", "D9")
          .getCy(DataCy.traceSaveSubmitButton)
          .should("be.disabled");
      });
    });

    describe("I can remove a rule on what types of artifacts a trace link is allowed between", () => {
      it("Can create a link after removing the rule blocking it", () => {
        cy.createNewTraceLink("F5", "D9")
          .getCy(DataCy.traceSaveSubmitButton)
          .should("be.disabled");

        // Delete the first link direction
        cy.getCy(DataCy.traceSaveModal).within(() => {
          cy.clickButton(DataCy.traceSaveDirectionsPanel);

          cy.getCy(DataCy.traceSaveDirectionsChip).each((el) => {
            cy.wrap(el).within(() => {
              cy.get("button").click();
            });
          });
        });

        cy.getCy(DataCy.traceSaveSubmitButton).should("be.enabled");
      });
    });
  });
});
