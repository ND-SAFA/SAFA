import { DataCy } from "@/fixtures";

describe("Artifact Subtree", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion();
  });

  describe("I can highlight an artifact’s subtree", () => {
    it("Highlights the selected subtree", () => {
      cy.selectArtifact("F11");

      // Selected node is visible.
      cy.getNodes(true)
        .should("be.visible")
        .should("not.have.css", "opacity", "0.3");

      // Subtree nodes are visible.
      cy.getNode("F9").should("not.have.css", "opacity", "0.3");
      cy.getNode("F15").should("not.have.css", "opacity", "0.3");
      cy.getNode("F17").should("not.have.css", "opacity", "0.3");

      // Unrelated node is faded.
      cy.getNode("D5").should("have.css", "opacity", "0.3");
    });
  });

  describe("I can hide an artifact’s subtree", () => {
    it("Hides the subtree below an artifact", () => {
      cy.centerGraph();

      // Assert that child node exists.
      cy.getNode("F17").should("be.visible");

      // Open the right click menu on the selected node, click to hide subtree.
      cy.getNode("F11").click().clickButton(DataCy.rightClickToggleSubtree);

      // Assert that subtree is hidden.
      cy.getNode("F17").should("not.be.visible");
    });
  });

  describe("I can show an artifact’s subtree", () => {
    it("Shows the subtree below an artifact", () => {
      cy.centerGraph();

      // Open the right click menu on the selected node, click to hide subtree.
      cy.getNode("F11").click().clickButton(DataCy.rightClickToggleSubtree);

      // Assert that subtree is hidden.
      cy.getNode("F17").should("not.be.visible");

      // Open the right click menu on the selected node, click to show subtree.
      cy.getNode("F11")
        .rightclick()
        .getCy(DataCy.rightClickToggleSubtree)
        .should("be.visible")
        .then(($el) => $el.click());

      // Assert that subtree is visible.
      cy.getNode("F17").should("be.visible");
    });
  });

  describe("I can see how many children are hidden below a parent artifact", () => {
    it("Shows the number of hidden children", () => {
      cy.centerGraph();

      // Open the right click menu on the selected node, click to hide subtree.
      cy.getNode("F11").click().clickButton(DataCy.rightClickToggleSubtree);

      // Assert that hidden children has correct count.
      cy.getNode("F11").should("have.attr", "data-cy-children", "6");
    });
  });
});
