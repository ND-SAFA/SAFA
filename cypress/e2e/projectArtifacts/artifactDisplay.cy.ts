import { DataCy } from "../../fixtures";

describe("Artifact Display", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
  });

  describe("I can select an artifact to view more details", () => {
    it.skip("Selects an artifact that is double clicked", () => {
      cy.centerGraph();

      // Double click node (doesnt allow chaining click).
      cy.getNodes().first().click().wait(10);
      cy.getNodes().first().click();

      // Affirm node is selected.
      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("be.visible");
    });
  });

  describe("I can see an artifacts type, name, and body", () => {
    it("Shows the artifact content of a selected artifact", () => {
      const artifactType = "design";
      const artifact = {
        name: "New",
        type: `${artifactType}{downArrow}{enter}`,
        body: "A New Artifact",
      };

      cy.createNewArtifact(artifact).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("contain", artifact.name);
      cy.getCy(DataCy.selectedPanelType).should("contain", artifactType);
      cy.getCy(DataCy.selectedPanelBody).should("contain", artifact.body);
      cy.getNodes(true).within(() => {
        cy.getCy(DataCy.treeNodeName).should("contain", artifact.name);
        cy.getCy(DataCy.treeNodeType).should("contain", artifactType);
        cy.getCy(DataCy.treeNodeBody).should("contain", artifact.body);
      });
    });
  });

  describe("I can see an artifacts parent and child artifacts", () => {
    it("I can see and select listed parent artifacts", () => {
      const parent = "D11";

      cy.createNewArtifact({
        parent: `${parent}{downArrow}{enter}`,
      }).saveArtifact();

      // Affirm created artifact is selected.
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.selectedPanelParents).should("be.visible");

      // Affirm parents are shown, and click first parent's link.
      cy.getCy(DataCy.selectedPanelParentItem)
        .should("have.length", 1)
        .first()
        .should("contain", parent)
        .within(() => {
          cy.clickButton(DataCy.selectedPanelParentLinkButton);
        });

      // Affirm link is visible and close.
      cy.getCy(DataCy.traceSourceButton).should("be.visible").click();

      // Affirm viewing parent artifact.
      cy.getCy(DataCy.selectedPanelParentItem)
        .first()
        .click()
        .getCy(DataCy.selectedPanelName)
        .should("contain", parent)
        .getCy(DataCy.treeSelectedNode)
        .within(() => {
          cy.getCy(DataCy.treeNodeName).should("contain", parent);
        });
    });

    it("I can see and select listed child artifacts", () => {
      const child = "New Artifact";
      const parent = "F21";

      cy.createNewArtifact({
        name: child,
        parent: `${parent}{downArrow}{enter}`,
      }).saveArtifact();

      // Affirm created artifact is selected, and select parent.
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.selectedPanelParents)
        .should("be.visible")
        .getCy(DataCy.selectedPanelParentItem)
        .first()
        .click();

      // Affirm children are shown, and click first child's link.
      cy.getCy(DataCy.selectedPanelChildren).should("be.visible");
      cy.getCy(DataCy.selectedPanelChildItem)
        .should("have.length", 1)
        .first()
        .should("contain", child)
        .within(() => {
          cy.clickButton(DataCy.selectedPanelChildLinkButton);
        });

      // Affirm link is visible and close.
      cy.getCy(DataCy.traceTargetButton).should("be.visible").click();

      // Affirm viewing created child artifact.
      cy.getCy(DataCy.selectedPanelChildItem)
        .first()
        .click()
        .getCy(DataCy.selectedPanelName)
        .should("contain", child)
        .getCy(DataCy.treeSelectedNode)
        .within(() => {
          cy.getCy(DataCy.treeNodeName).should("contain", child);
        });
    });
  });
});
