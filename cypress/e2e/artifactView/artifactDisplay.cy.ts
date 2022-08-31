import { DataCy } from "../../fixtures";

describe("Artifact Display", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
  });

  describe("I can select an artifact to view more details", () => {
    it("Selects an artifact that is double clicked", () => {
      cy.getNodes().first().click();
      cy.getNodes().first().click();

      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelName).should("be.visible");
    });
  });

  describe("I can see an artifacts type, name, and body", () => {
    it("Shows the artifact content of a selected artifact", () => {
      const artifactType = "Design";
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
      cy.getCy(DataCy.treeNodeName).should("contain", artifact.name);
      cy.getCy(DataCy.treeNodeType).should("contain", artifactType);
      cy.getCy(DataCy.treeNodeBody).should("contain", artifact.body);
    });
  });

  describe("I can see an artifacts parent and child artifacts", () => {
    it("I can see and select listed parent artifacts", () => {
      const parent = "D11";

      cy.createNewArtifact({
        parent: `${parent}{downArrow}{enter}`,
      }).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.selectedPanelParents).should("be.visible").click();

      cy.getCy(DataCy.selectedPanelParentItem)
        .should("have.length", 1)
        .first()
        .should("contain", parent)
        .within(() => {
          cy.clickButton(DataCy.selectedPanelParentLinkButton);
        });

      cy.getCy(DataCy.traceApproveModal)
        .should("be.visible")
        .closeModal(DataCy.traceApproveModal);

      cy.getCy(DataCy.selectedPanelParentItem)
        .first()
        .click()
        .getCy(DataCy.selectedPanelName)
        .should("contain", parent);
    });

    it("I can see and select listed child artifacts", () => {
      const child = "New Artifact";
      const parent = "F21";

      cy.createNewArtifact({
        name: child,
        parent: `${parent}{downArrow}{enter}`,
      }).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.selectedPanelParents)
        .should("be.visible")
        .click()
        .getCy(DataCy.selectedPanelParentItem)
        .first()
        .click();

      cy.getCy(DataCy.selectedPanelChildren)
        .should("be.visible")
        .getCy(DataCy.selectedPanelChildItem)
        .should("have.length", 1)
        .first()
        .should("contain", child)
        .within(() => {
          cy.clickButton(DataCy.selectedPanelChildLinkButton);
        });

      cy.getCy(DataCy.traceApproveModal)
        .should("be.visible")
        .closeModal(DataCy.traceApproveModal);

      cy.getCy(DataCy.selectedPanelChildItem)
        .first()
        .click()
        .getCy(DataCy.selectedPanelName)
        .should("contain", child);
    });
  });
});
