import { DataCy } from "@/fixtures";

describe("Trace Links", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion();
  });

  describe("I can create a new trace link", () => {
    it("Creates a new trace link", () => {
      cy.createNewTraceLink("D3", "F5", true);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("I can delete a trace link", () => {
    it("Deletes a trace link", () => {
      cy.createNewArtifact(
        {
          parent: "{downArrow}{enter}",
        },
        true
      );

      cy.getCy(DataCy.selectedPanelParents).should("be.visible");
      cy.getCy(DataCy.selectedPanelParentItem)
        .first()
        .within(() => {
          cy.clickButton(DataCy.selectedPanelParentLinkButton);
        });

      cy.clickButton(DataCy.traceDeleteButton).clickButton(
        DataCy.confirmModalButton
      );

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.selectedPanelParents).should("not.exist");
    });
  });
});
