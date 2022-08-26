import { DataCy, validUser } from "../fixtures";

describe("Artifact View", () => {
  beforeEach(() => {
    // TODO: clean up existing projects and create a new one.

    cy.visit("/").login(validUser.email, validUser.password);

    cy.location("pathname", { timeout: 5000 }).should("equal", "/");

    cy.openProjectSelector()
      .projectSelectorContinue()
      .projectSelectorContinue();

    cy.location("pathname", { timeout: 5000 }).should("equal", "/project");
  });

  describe("Artifact CRUD", () => {
    describe("I can create a new artifact", () => {
      it("Creates a simple new artifact", () => {
        cy.createNewArtifact();

        cy.getCy(DataCy.artifactSaveModal).within(() => {
          cy.clickButton(DataCy.artifactSaveSubmitButton);
        });

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");

        cy.getCy(DataCy.artifactTreeSelectedNode).should("be.visible");
      });

      it("Cannot create an artifact without a name, type, or body", () => {
        cy.createNewArtifact("");

        cy.getCy(DataCy.artifactSaveModal).within(() => {
          cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");

          cy.inputText(DataCy.artifactSaveNameInput, `New ${Math.random()}`);
          cy.getCy(DataCy.artifactSaveBodyInput).clear();

          cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");

          cy.inputText(DataCy.artifactSaveBodyInput, "New Artifact");
          cy.getCy(DataCy.artifactSaveTypeInput).clear();

          cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");

          cy.inputText(
            DataCy.artifactSaveTypeInput,
            "Designs{downArrow}{enter}"
          );

          cy.getCy(DataCy.artifactSaveSubmitButton).should("be.enabled");
        });
      });

      // it("Cannot create a new artifact with the same name", () => {})

      // it("Creates an artifact with a new type", () => {})
    });
  });
});
