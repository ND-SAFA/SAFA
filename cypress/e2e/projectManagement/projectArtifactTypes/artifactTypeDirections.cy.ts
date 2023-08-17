import { DataCy } from "@/fixtures";

describe("Artifact Type Directions", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion();
  });

  describe("I cannot create trace links between types in both directions", () => {
    it("Cannot create links from an artifact to itself", () => {
      cy.createNewTraceLink()
        .getCy(DataCy.traceSaveSubmitButton)
        .should("be.disabled");
    });

    it("Cannot create an existing link", () => {
      cy.createNewTraceLink("F15", "F9")
        .getCy(DataCy.traceSaveSubmitButton)
        .should("be.disabled");
    });

    it("Cannot create a link in an invalid direction", () => {
      cy.createNewTraceLink("F5", "D9")
        .getCy(DataCy.traceSaveSubmitButton)
        .should("be.disabled");
    });
  });

  describe("I can remove a rule on what types of artifacts a trace link is allowed between", () => {
    it.only("Can create a link after removing the rule blocking it", () => {
      cy.clickButton(DataCy.artifactFabToggle).clickButton(
        DataCy.artifactFabCreateTrace
      );

      cy.inputText(DataCy.traceSaveSourceInput, `F5{downArrow}{enter}`);

      // Show hidden types.
      cy.clickButton(DataCy.traceSaveTargetInput)
        .getCy("button-filter-type")
        .filter(":visible")
        .filter(".nav-mode-selected")
        .each(($el) => $el.click());

      cy.inputText(DataCy.traceSaveTargetInput, `D9{downArrow}{enter}{esc}`);

      cy.getCy(DataCy.traceSaveSubmitButton).should("be.disabled");

      // Delete the first link direction.
      cy.clickButton(DataCy.traceSaveDirectionsPanel);

      cy.getCy(DataCy.traceSaveDirectionsChip).each((el) => {
        cy.wrap(el).within(() => {
          cy.get("i").click({ multiple: true });
        });
      });

      cy.getCy(DataCy.traceSaveSubmitButton).should("be.enabled");
    });
  });
});
