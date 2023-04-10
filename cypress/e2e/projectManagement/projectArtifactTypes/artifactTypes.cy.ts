import { DataCy } from "@/fixtures";

describe("Artifact Types", () => {
  before(() => {
    cy.initProject();
  });

  beforeEach(() => {
    cy.initProjectVersion();
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
    it.only("Changes the icon of a type", () => {
      const type = "Design";

      cy.switchToTimView();

      cy.getNode(type).click();
      cy.getCy(DataCy.typeOptionsIconButton).within(() => {
        cy.get("button").last().click();
      });

      cy.getCy(DataCy.artifactLevelContent).within(() => {
        cy.get("i").first().should("have.class", "mdi-alpha-a-box-outline");
      });
    });
  });
});
