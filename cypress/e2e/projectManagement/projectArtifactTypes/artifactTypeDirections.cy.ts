import { DataCy } from "@/fixtures";

describe("Artifact Type Directions", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion();
  });

  describe("I cannot create trace links between types in both directions", () => {
    it("Cannot create restricted links", () => {
      // Selects two of the same artifact.
      cy.createNewTraceLink()
        .getCy(DataCy.traceSaveSubmitButton)
        .should("be.disabled");

      // Selects an existing link.
      cy.fillTraceLinkFields("F15", "F9")
        .getCy(DataCy.traceSaveSubmitButton)
        .should("be.disabled");

      // Selects an invalid link direction.
      cy.fillTraceLinkFields("F5", "D9")
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
      cy.clickButton(DataCy.traceSaveDirectionsPanel);

      cy.getCy(DataCy.traceSaveDirectionsChip).each((el) => {
        cy.wrap(el).within(() => {
          cy.get("button").click();
        });
      });

      cy.getCy(DataCy.traceSaveSubmitButton).should("be.enabled");
    });
  });
});
