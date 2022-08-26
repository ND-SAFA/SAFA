/* eslint-disable max-lines */
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
      });
    });

    describe("I can delete artifacts", () => {
      it("Can delete artifacts", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");
        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - opens up artifact drop box and deletes artifact
        cy.clickButton(DataCy.creationArtifactButton);
        cy.clickButton(DataCy.creationArtifactDeleteButton);
      });

      it("Cannot continue after deleted valid artifacts", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");
        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);
        // Step - opens up artifact drop box and deletes artifact
        cy.clickButton(DataCy.creationArtifactButton);
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
        cy.clickButton(DataCy.creationArtifactButton);
        cy.clickButton(DataCy.creationEntitiesButton);
      });
    });

    describe("I can upload a file containing the artifacts I want to create", () => {
      it("Can continue after uploading artifacts", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");
        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Can continue after uploading artifact
        cy.clickButton(DataCy.stepperContinueButton);
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
        cy.clickButton(DataCy.stepperContinueButton);
      });
    });
  });

  describe("Project Trace Link Uploading", () => {
    describe("I can create sets of trace links between two artifact types", () => {
      it("Can create a new panel of trace links", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Creates Trace Matrix, Selects source + target w/ artifact of users choice
        cy.createTraceMatrix("requirement", "hazard");

        // Step -Can create a new panel of trace links
        cy.clickButtonWithName("Create trace matrix");
      });

      it("Cannot create a new panel without selecting two artifact types", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Checks that the user cannot create a new panel without selecting two artifact types
        cy.clickButton(DataCy.stepperContinueButton);
        cy.clickButtonWithName("Create new trace matrix");
        cy.contains("Create new trace matrix").should("be.disabled");
      });
    });

    describe("I can delete a set of trace links", () => {
      it("Can delete a set of trace links", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - creates Trace Matrix, Selects source + target w/ artifact of users choice
        cy.createTraceMatrix("requirement", "hazard");

        // Step - Create trace matrix panel
        cy.clickButtonWithName("Create trace matrix");

        // Step - being able to delete a set of trace links
        cy.clickButton("button-delete-artifact", "last");
      });
    });

    describe("I can preview the list of trace links loaded from a file", () => {
      it("Displays buttons for all of the trace links in the file", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - creates Trace Matrix, Selects source + target w/ artifact of users choice
        cy.createTraceMatrix("requirement", "hazard");

        // Step - Uploads trace link files
        cy.uploadingTraceLinks(simpleProjectFilesMap.requirement2hazard);

        // Step - going back a tab and opening dropbox to check entities
        cy.clickButtonWithName("Go back");
        cy.clickButtonWithName("requirement-hazard");

        // Step - making sure entities are viewable
        cy.clickButton(DataCy.creationEntitiesButton, "last");
      });
    });

    describe("I can upload a file containing the trace links I want to create", () => {
      it("Can continue with no trace links", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - Creates Empty design2design artifact
        cy.createArtifactPanel("Empty Design", testFileMap.Emptydesign2design);
        cy.clickButton(DataCy.creationIgnoreErrorsButton, undefined);

        // Step - Creates Empty design artifact
        cy.createArtifactPanel("Empty design", testFileMap.Emptydesign);

        // Step - Ignores errors
        //cy.clickButton(DataCy.creationIgnoreErrorsButton, "last");

        // Step - Creates Trace Matrix, Selects source + target w/ artifact of users choice
        cy.createTraceMatrix("design", "design");

        // Step - Uploads trace link files (Emptydesign2design)
        cy.uploadingTraceLinks(testFileMap.Emptydesign2design);
      });

      it("Can continue after uploading trace links", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Creates Trace Matrix, Selects source + target w/ artifact of users choice
        cy.createTraceMatrix("requirement", "hazard");

        // Step - Uploads trace link files (requirement2hazard)
        cy.uploadingTraceLinks(simpleProjectFilesMap.requirement2hazard);
      });

      it("Can continue with a bad file if errors are ignored", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - creates hazard2hazard artifact
        cy.createArtifactPanel(
          "hazard2hazard",
          simpleProjectFilesMap.hazard2hazard
        );

        // Step - Ignore errors
        cy.clickButton(DataCy.creationIgnoreErrorsButton, "last");

        // Step - Creates Trace Matrix, Selects source + target w/ artifact of users choice
        cy.createTraceMatrix("hazard", "hazard");

        // Step - Uploads trace link files (hazard2hazard)
        cy.uploadingTraceLinks(simpleProjectFilesMap.hazard2hazard);
      });
    });

    describe("I can generate trace links between artifacts", () => {
      it("Can continue with trace links set to be generated", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - Creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - Creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Creates Trace Matrix, Selects source + target w/ artifact of users choice
        cy.createTraceMatrix("requirement", "hazard");

        // Step - Creates trace matrix
        cy.clickButtonWithName("Create trace matrix");

        // Step - Able to generate Trace Links and continue
        cy.clickButtonWithName("Generate Trace Links");
      });
    });
  });

  describe("Project Tim Preview", () => {
    it("Displays artifact types on the graph", () => {
      // Step - Inputs Project name and description
      cy.setProjectIdentifier("standard");

      // Step - Creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - Creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - Creates Trace Matrix, Selects source + target w/ artifact of users choice
      cy.createTraceMatrix("requirement", "hazard");

      // Step - Uploads trace link files (requirement2hazard)
      cy.uploadingTraceLinks(simpleProjectFilesMap.requirement2hazard);

      // Step - Checks that correct artifacts are displayed in the Tim Tree
      cy.contains("Hazard");
      cy.contains("Requirement");
    });

    it.skip("Displays trace links between artifact types on the graph", () => {
      // Step - Inputs Project name and description
      cy.setProjectIdentifier("standard");

      // Step - creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - creates Trace Matrix, Selects source + target w/ artifact of users choice
      cy.createTraceMatrix("requirement", "hazard");

      // Step - Uploads trace link files
      cy.uploadingTraceLinks(simpleProjectFilesMap.requirement2hazard);

      // Step - Checks the displayed Trace Links between artifacts
      cy.contains("5");
    });

    it.skip("Displays all nodes on the graph within the current view", () => {
      // Step - Inputs Project name and description
      cy.setProjectIdentifier("standard");

      // Step - creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - creates Trace Matrix, Selects source + target w/ artifact of users choice
      cy.createTraceMatrix("requirement", "hazard");

      // Step - Uploads trace link files
      cy.uploadingTraceLinks(simpleProjectFilesMap.requirement2hazard);

      // Step - Checks that there are the correct number of nodes within each artifact
      cy.contains("5 Nodes");
      cy.contains("5 Nodes");
    });

    it.skip("Displays the correct count of artifacts and links", () => {
      // Step - Inputs Project name and description
      cy.setProjectIdentifier("standard");

      // Step - creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - creates Trace Matrix, Selects source + target w/ artifact of users choice
      cy.createTraceMatrix("requirement", "hazard");

      // Step - Uploads trace link files
      cy.uploadingTraceLinks(simpleProjectFilesMap.requirement2hazard);

      // Step - Checks for display of Artifacts, Nodes and Trace Links within the Tim Tree
      cy.contains("hazard");
      cy.contains("Requirement");
      cy.contains("5");
      cy.contains("5 Nodes");
    });
  });

  describe("I can manually create a Project", () => {
    it.skip("Can create a project with valid data", () => {
      // Step - Inputs Project name and description
      cy.setProjectIdentifier("standard");

      // Step - creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - creates Trace Matrix, Selects source + target w/ artifact of users choice
      cy.createTraceMatrix("requirement", "hazard");

      // Step - Uploads trace link files
      cy.uploadingTraceLinks(simpleProjectFilesMap.requirement2hazard);

      // Step - Checks for display of Artifacts, Nodes and Trace Links within the Tim Tree
      cy.contains("hazard");
      cy.contains("Requirement");
      cy.contains("5");
      cy.contains("5 Nodes");

      // Step - Finalizes project by creating it
      cy.clickButtonWithName("Create Project");
    });
  });
});
