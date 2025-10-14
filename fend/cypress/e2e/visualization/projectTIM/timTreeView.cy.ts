describe("TIM Tree View", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion().switchToTimView();
  });

  describe("I can see the TIM tree of a document", () => {
    it("Shows all TIM artifact types", () => {
      cy.getNode("Design")
        .should("be.visible")
        .within(() => {
          cy.contains("14 Artifacts");
        });

      cy.getNode("Requirement")
        .should("be.visible")
        .within(() => {
          cy.contains("5 Artifacts");
        });
    });
  });
});
