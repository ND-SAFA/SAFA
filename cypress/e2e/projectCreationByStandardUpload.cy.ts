import {
  DataCy,
  simpleProjectFilesMap,
  testFileMap,
  testProject,
  validUser,
} from "../fixtures";

describe("Project Creation", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080/create").login(
      validUser.email,
      validUser.password
    );

    cy.location("pathname", { timeout: 5000 }).should("equal", "/create");
  });

  describe("Manual Project Creation", () => {
    describe("Project Artifact Uploading", () => {
      it("Cannot create a project without a name", () => {
        // Step - inputting description
        cy.inputText(
          DataCy.creationStandardDescriptionInput,
          testProject.description
        );

        // Step - Checking that the user cannot continue without a project name
        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
      });
    });

    describe("I can Create sets of artifacts by type", () => {
      it("Cannot create a new panel with an empty name", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - Checking user cannot create a new panel without an artifact name
        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.getCy(DataCy.creationCreatePanelButton).should("be.disabled");
      });

      it("Can create a new panel of artifacts", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);
        //Step - Able to create a new panel after creating an artifact
        cy.clickButton(DataCy.creationCreatePanelButton);

        cy.getCy(DataCy.creationFilePanel).should("be.visible");
      });
    });

    describe("I can delete artifacts", () => {
      it("Can delete artifacts", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");
        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - opens up artifact drop box and deletes artifact
        cy.openPanelAfterClose();
        cy.clickButton(DataCy.creationArtifactDeleteButton);

        cy.getCy(DataCy.creationFilePanel).should("not.exist");
      });

      it("Cannot continue after deleted valid artifacts", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");
        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - opens up artifact drop box and deletes artifact
        cy.openPanelAfterClose();
        cy.clickButton(DataCy.creationArtifactDeleteButton);

        // Step - Cannot continue after artifact is deleted
        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
      });
    });

    describe("I can preview the list of artifacts loaded from a file", () => {
      it("Displays buttons for all of the artifacts in the file", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Opens up artifact dropbox and is able to view entities within artifact
        cy.openPanelAfterClose();

        // Step - making sure entities are viewable
        cy.getCy(DataCy.creationEntitiesButton)
          .should("be.visible")
          .clickButton(DataCy.creationEntitiesButton, "last");

        cy.getCy(DataCy.creationEntityButton).should("have.length", 5);
      });
    });

    describe("I can upload a file containing the artifacts I want to create", () => {
      it("Can continue after uploading artifacts", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");
        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Can continue after uploading artifact
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
      });

      it("Can continue with bad file if errors are ignored", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");
        // Step - Creating a bad artifact file
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement2requirement
        );

        // Step - Pressing ignore errors so user can continue
        cy.clickButton(DataCy.creationIgnoreErrorsButton, undefined);

        // Step - Can continue after ignoring errors
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
      });
    });
  });

  describe("Project Trace Link Uploading", () => {
    describe("I can create sets of trace links between two artifact types", () => {
      it("Can create a new panel of trace links", () => {
        cy.createReqToHazardFiles();

        // Step - Creates Trace Matrix, Selects source + target w/ artifact of users choice
        cy.createTraceMatrix("requirement", "hazard");

        cy.getCy(DataCy.creationFilePanel).should("be.visible");
      });

      it("Cannot create a new panel without selecting two artifact types", () => {
        cy.createReqToHazardFiles();

        // Step - Checks that the user cannot create a new panel without selecting two artifact types
        cy.clickButtonWithName("Create new trace matrix");

        cy.contains("Create new trace matrix").should("be.disabled");
      });
    });

    describe("I can delete a set of trace links", () => {
      it("Can delete a set of trace links", () => {
        cy.createReqToHazardFiles(true);

        // Step - being able to delete a set of trace links
        cy.openPanelAfterClose();
        cy.clickButton(DataCy.creationDeletePanel, "last");

        cy.contains("requirement X hazard").should("not.exist");
      });
    });

    describe("I can preview the list of trace links loaded from a file", () => {
      it("Displays buttons for all of the trace links in the file", () => {
        cy.createReqToHazardFiles(true);

        // Step -  Open the entity dropbox
        cy.openPanelAfterClose();

        // Step - making sure entities are viewable
        cy.getCy(DataCy.creationEntitiesButton)
          .should("be.visible")
          .clickButton(DataCy.creationEntitiesButton, "last");

        cy.getCy(DataCy.creationEntityButton).should("have.length", 5);
      });
    });

    describe("I can upload a file containing the trace links I want to create", () => {
      it("Can continue with no trace links", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - Creates Empty design2design artifact
        cy.createArtifactPanel("Empty Design", testFileMap.emptyDesign2Design);
        cy.clickButton(DataCy.creationIgnoreErrorsButton, undefined);

        // Step - Creates Empty design artifact
        cy.createArtifactPanel("Empty design", testFileMap.emptyDesign, true);

        // Step - Creates Trace Matrix, Selects source + target w/ artifact of users choice
        cy.createTraceMatrix(
          "design",
          "design",
          testFileMap.emptyDesign2Design
        );

        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
      });

      it("Can continue after uploading trace links", () => {
        cy.createReqToHazardFiles(true);

        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
      });

      it("Can continue with a bad file if errors are ignored", () => {
        cy.createReqToHazardFiles();

        // Step - Creates Trace Matrix, Selects source + target w/ artifact of users choice
        cy.createTraceMatrix("hazard", "hazard");

        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");

        // Step - Ignore errors
        cy.clickButton(DataCy.creationIgnoreErrorsButton, "last");

        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
      });
    });

    describe("I can generate trace links between artifacts", () => {
      it("Can continue with trace links set to be generated", () => {
        cy.createReqToHazardFiles();

        // Step - Creates Trace Matrix, Selects source + target w/ artifact of users choice
        cy.createTraceMatrix("requirement", "hazard");

        cy.openPanelAfterClose();

        // Step - Able to generate Trace Links and continue
        cy.clickButtonWithName("Generate Trace Links");

        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
      });
    });
  });

  describe("Project Tim Preview", () => {
    beforeEach(() => {
      // Step - Create project with requirements and hazards.
      cy.createReqToHazardFiles(true, true);
    });

    it("Displays all nodes on the graph within the current view", () => {
      // Step - Checks that there are the correct number of nodes within each artifact
      cy.get(".artifact-svg-wrapper")
        .should("be.visible")
        .within(() => {
          cy.contains("text", "requirement").should("be.visible");
          cy.contains("text", "hazard").should("be.visible");
          cy.contains("text", "5 Nodes").should("be.visible");
        });
    });

    it.skip("Displays trace links between artifact types on the graph", () => {
      // Wait for graph to load.
      cy.getCy(DataCy.appLoading).should("be.visible");
      cy.get(".artifact-svg-wrapper").should("be.visible");

      // Step - Checks the displayed Trace Links between artifacts & their counts
      // TODO: set up screenshot comparisons: https://valor-software.com/articles/testing-canvas-could-be-easier.html
      cy.get("canvas").last().screenshot();
    });
  });

  describe("I can manually create a Project", () => {
    it("Can create a project with valid data", () => {
      cy.createReqToHazardFiles(true, true);

      // Step - Finalizes project by creating it
      cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled").click();

      // Step - Check for creation success message
      cy.getCy(DataCy.snackbarSuccess).should("be.visible");

      cy.clickButton(DataCy.jobPanel).clickButton(DataCy.jobDeleteButton);
    });
  });
});
