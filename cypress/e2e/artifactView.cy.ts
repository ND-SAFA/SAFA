import { DataCy, validUser } from "../fixtures";

describe("Artifact View", () => {
  before(() => {
    cy.dbResetJobs();
    cy.dbResetProjects();

    cy.visit("/create").login(validUser.email, validUser.password);

    cy.location("pathname", { timeout: 5000 }).should("equal", "/create");

    cy.createBulkProject()
      .getCy(DataCy.jobStatus, "first", 20000)
      .should("contain.text", "Completed");

    cy.logout();
  });

  beforeEach(() => {
    cy.visit("/project").login(validUser.email, validUser.password);

    cy.location("pathname", { timeout: 5000 }).should("equal", "/project");

    cy.get(".artifact-svg-wrapper").should("be.visible");
  });

  describe("Artifact CRUD", () => {
    describe("I can create a new artifact", () => {
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

      it("Cannot create a new artifact with the same name", () => {
        const name = `New ${Math.random()}`;

        cy.createNewArtifact(name);

        cy.getCy(DataCy.artifactSaveModal).within(() => {
          cy.clickButton(DataCy.artifactSaveSubmitButton);
        });

        cy.createNewArtifact(name);

        cy.getCy(DataCy.artifactSaveModal).within(() => {
          cy.contains("Name is already used");
          cy.getCy(DataCy.artifactSaveSubmitButton).should("be.disabled");
        });
      });

      it("Creates a simple new artifact", () => {
        const name = `New ${Math.random()}`;

        cy.createNewArtifact(name);

        cy.getCy(DataCy.artifactSaveModal).within(() => {
          cy.clickButton(DataCy.artifactSaveSubmitButton);
        });

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        cy.getCy(DataCy.artifactTreeSelectedNode).should("be.visible");
        cy.getCy(DataCy.artifactTreeSelectedName).should("contain", name);
      });

      it("Creates a new artifact from the right click menu", () => {
        const name = `New ${Math.random()}`;

        // Opens the right click window.
        cy.get("canvas")
          .first()
          .then(($el) =>
            cy.wrap($el).rightclick($el.width() / 4, $el.height() / 4)
          );

        // Click the add artifact button.
        cy.get("#add-artifact")
          .should("be.visible")
          .then(($el) => $el.click());

        cy.fillArtifactModal(name);

        cy.getCy(DataCy.artifactSaveModal).within(() => {
          cy.clickButton(DataCy.artifactSaveSubmitButton);
        });

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        cy.getCy(DataCy.artifactTreeSelectedNode).should("be.visible");
        cy.getCy(DataCy.artifactTreeSelectedName).should("contain", name);
      });

      it.only("Creates an artifact with a new type", () => {
        const name = `New ${Math.random()}`;

        cy.createNewArtifact(name, "New Type{enter}");

        cy.getCy(DataCy.artifactSaveModal).within(() => {
          cy.clickButton(DataCy.artifactSaveSubmitButton);
        });

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        cy.getCy(DataCy.artifactTreeSelectedNode).should("be.visible");
        cy.getCy(DataCy.artifactTreeSelectedName).should("contain", name);
      });
    });
  });
});
