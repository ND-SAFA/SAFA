import { DataCy } from "@/fixtures";

describe("Artifact Tree Nodes & Edges", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion();
  });

  describe("I can select an artifact to view more details", () => {
    it("Selects an artifact that is clicked", () => {
      cy.centerGraph();

      cy.getNodes().first().click();

      // Affirm node is selected.
      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("be.visible");
    });
  });

  describe.skip("I can select a trace link to view more details", () => {
    it("Selects a trace link that is clicked", () => {
      cy.centerGraph();

      cy.getNode("F6").then(($el1) => {
        cy.getNode("D3").then(($el2) => {
          cy.get("body").click(
            Math.abs($el1.position().top - $el2.position().top),
            Math.abs($el1.position().left - $el2.position().left)
          );
        });
      });

      // Affirm edge is selected.
      cy.getCy(DataCy.selectedPanelName).should("be.visible");
    });
  });
});
