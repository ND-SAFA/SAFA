import { DataCy } from "@/fixtures";

describe("Artifact Types", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion().expandViewport();
  });

  describe("I can add a new artifact type when creating a new artifact", () => {
    it("Creates an artifact with a new type", () => {
      const type = "New Type";

      cy.createNewArtifact({ type: `${type}{enter}` }, true);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.getCy(DataCy.selectedPanelType).should("contain", type);

      cy.clickButton(DataCy.selectedPanelCloseButton).switchToTimView();

      cy.getNode(type).should("be.visible");

      cy.switchToTimView();

      cy.getNode(type).should("be.visible");
    });
  });

  describe("I can change the icon of an artifact type", () => {
    it("Changes the icon of a type", () => {
      const type = "design";

      cy.switchToTimView();

      cy.getNode(type).click();
      cy.getCy(DataCy.typeOptionsIconButton).last().click();

      cy.getCy(DataCy.artifactLevelContent).within(() => {
        cy.get("i").should("have.class", "mdi-alpha-a-box-outline");
      });
    });
  });
});
