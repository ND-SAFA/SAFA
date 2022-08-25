import { DataCy, validUser } from "../fixtures";

describe("Artifact View", () => {
  beforeEach(() => {
    // TODO: clean up existing projects and create a new one.

    cy.visit("/").login(validUser.email, validUser.password);

    cy.location("pathname", { timeout: 2000 }).should("equal", "/");

    cy.openProjectSelector()
      .projectSelectorContinue()
      .projectSelectorContinue();

    cy.location("pathname", { timeout: 2000 }).should("equal", "/project");
  });

  describe("Artifact CRUD", () => {
    describe("I can create a new artifact", () => {
      it("Creates a simple new artifact", () => {
        cy.createNewArtifact();

        cy.getCy(DataCy.artifactSaveModal).within(() => {
          cy.clickButton(DataCy.artifactSaveSubmitButton);
        });

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      });

      // it("Centers on the new artifact", () => {})

      it("Cannot create an artifact without a name", () => {
        cy.createNewArtifact("");

        cy.getCy(DataCy.artifactSaveModal).within(() => {
          cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");
        });
      });

      it("Cannot create an artifact without a description", () => {
        cy.createNewArtifact(
          `New ${Math.random()}`,
          "Designs{downArrow}{enter}",
          ""
        );

        cy.getCy(DataCy.artifactSaveModal).within(() => {
          cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");
        });
      });

      it("Cannot create an artifact without a type", () => {
        cy.createNewArtifact(`New ${Math.random()}`, "");

        cy.getCy(DataCy.artifactSaveModal).within(() => {
          cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");
        });
      });

      // it("Cannot create a new artifact with the same name", () => {})

      // it("Creates an artifact with a new type", () => {})
    });
  });
});
