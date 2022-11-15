import { DataCy } from "../../fixtures";

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

      cy.clickButtonWithName("Settings").switchTab("Artifact Settings");
      cy.getCy(DataCy.typeOptionsList).should("contain", type);
    });
  });

  describe("I can change the icon of an artifact type", () => {
    it("Changes the icon of a type", () => {
      cy.clickButtonWithName("Settings").switchTab("Artifact Settings");

      cy.getCy(DataCy.typeOptionsList)
        .first()
        .click()
        .within(() => {
          cy.getCy(DataCy.typeOptionsIconButton).first().click();
          cy.get("i").should("have.class", "mdi-clipboard-text");
        });
    });
  });
});
