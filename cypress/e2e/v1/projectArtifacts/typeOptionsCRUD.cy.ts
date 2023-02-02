import { DataCy } from "../../../fixtures";

describe("Type Options CRUD", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.viewport(1024, 768);
    cy.loadCurrentProject();
  });

  describe("I can add a new artifact type when creating a new artifact", () => {
    it("Creates an artifact with a new type", () => {
      const type = "New Type";

      cy.createNewArtifact({ type: `${type}{enter}` }).saveArtifact();

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getNodes(true).should("be.visible");
      cy.getCy(DataCy.selectedPanelType).should("contain", type);

      cy.clickButton(DataCy.selectedPanelCloseButton).clickButton(
        DataCy.navTimButton
      );

      cy.getNode(type).should("be.visible");
    });
  });

  describe("I can change the icon of an artifact type", () => {
    it("Changes the icon of a type", () => {
      const type = "design";

      cy.clickButton(DataCy.navTimButton);

      cy.getNode(type).click();
      cy.getCy(DataCy.typeOptionsIconButton).last().click();

      cy.getCy(DataCy.artifactLevelContent).within(() => {
        cy.get("i").should("have.class", "mdi-alpha-a-box-outline");
      });
    });
  });
});
