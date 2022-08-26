/* eslint-disable max-lines */
import {
  DataCy,
  simpleProjectFilesMap,
  testFileMap,
  testProject,
  // eslint-disable-next-line prettier/prettier
  validUser
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
      it("cannot create a project without a name", () => {
        cy.inputText(
          DataCy.creationStandardDescriptionInput,
          testProject.description
        );

        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
      });
    });

    describe("I can Create sets of artifacts by type", () => {
      it("cannot create a new panel with an empty name", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.getCy(DataCy.creationCreatePanelButton).should("be.disabled");
      });
      it("can create a new panel of artifacts", () => {
        cy.setProjectIdentifier("standard");

        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        cy.clickButton(DataCy.creationCreatePanelButton);
      });
    });

    describe("I can delete artifacts", () => {
      it("can delete artifacts", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - opens up artifact drop box and deletes artifact
        cy.clickButton(DataCy.creationArtifactButton);
        cy.clickButton(DataCy.creationArtifactDeleteButton);
      });
      it("cannot continue after deleted", () => {
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
      it("displays buttons for all of the artifacts in the file", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        cy.clickButton(DataCy.creationArtifactButton);
        cy.clickButton(DataCy.creationEntitiesButton);
      });
    });

    describe("I can upload a file containing the artifacts I want to create", () => {
      it("can continue after uploading artifacts", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        cy.clickButton(DataCy.stepperContinueButton);
      });
      it("can continue with bad file if errors are ignored", () => {
        cy.setProjectIdentifier("standard");
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement2requirement
        );

        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
        cy.clickButton(DataCy.creationIgnoreErrorsButton, undefined);
        cy.clickButton(DataCy.stepperContinueButton);
      });
    });
  });

  describe("Project Trace Link Uploading", () => {
    describe("I can create sets of trace links between two artifact types", () => {
      it("can create a new panel of trace links", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Creates Trace Matrix, just type the types of artifact
        cy.createTraceMatrix("requirement", "hazard");

        cy.clickButtonWithName("Create trace matrix");
      });
    });
    describe("I can delete a set of trace links", () => {
      it("can delete a set of trace links", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - creates Trace Matrix, just type the types of artifact
        cy.createTraceMatrix("requirement", "hazard");

        // Step - Create trace matrix panel
        cy.clickButtonWithName("Create trace matrix");

        // Step - being able to delete a set of trace links
        cy.clickButton("button-delete-artifact", "last");
      });
    });

    describe("I can preview the list of trace links loaded from a file", () => {
      it("displays buttons for all of the trace links in the file", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - creates Trace Matrix, just type the types of artifact
        cy.createTraceMatrix("requirement", "hazard");

        // Step - Uploads trace link files
        cy.uploadingTraceLinks(simpleProjectFilesMap.requirement2hazard);

        cy.clickButtonWithName("Go back");

        // Step - opening dropbox to check entities
        cy.clickButtonWithName("requirement-hazard");

        // Step - making sure entities are viewable
        cy.clickButton(DataCy.creationEntitiesButton, "last");
      });
    });
    // NEED THE BEFORE EACH TO STOP WORKING FOR THIS TEST DUE TO DIFFERENT ARTIFACTS USED ---------------------------------------------
    describe("I can upload a file containing the trace links I want to create", () => {
      it("can continue with no trace links", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        cy.createArtifactPanel("Empty Design", testFileMap.Emptydesign2design);
        cy.clickButton(DataCy.creationIgnoreErrorsButton, undefined);

        cy.createArtifactPanel(
          "Design2design",
          simpleProjectFilesMap.design2design
        );

        cy.clickButton(DataCy.creationIgnoreErrorsButton, "last"); // IGNORE BUTTONS ISNT WORKING

        // Step - Move to step 3 (creating trace panels)

        // Step - creates Trace Matrix, just type the types of artifact
        cy.createTraceMatrix("design", "design");

        // Step - Uploads trace link files
        cy.uploadingTraceLinks(testFileMap.Emptydesign2design);
      });
      it("can continue after uploading trace links", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - creates Trace Matrix, just type the types of artifact
        cy.createTraceMatrix("requirement", "hazard");

        // Step - Uploads trace link files
        cy.uploadingTraceLinks(simpleProjectFilesMap.requirement2hazard);
      });

      it("can continue with a bad file if errors are ignored", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - creates hazard artifact - type artifact and file
        cy.createArtifactPanel(
          "hazard2hazard",
          simpleProjectFilesMap.hazard2hazard
        );

        cy.clickButton(DataCy.creationIgnoreErrorsButton, "last");

        // Step - creates Trace Matrix, just type the types of artifact
        cy.createTraceMatrix("hazard", "hazard");

        // Step - Uploads trace link files
        cy.uploadingTraceLinks(simpleProjectFilesMap.hazard2hazard);

        //Step - being able to continue after ignoring errors from hazard2hazard errors
        //cy.clickButton(DataCy.creationIgnoreErrorsButton, "last");
      });
    });
    describe("I can generate trace links between artifacts", () => {
      it("can continue with trace links set to be generated", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - creates Trace Matrix, just type the types of artifact
        cy.createTraceMatrix("requirement", "hazard");

        // Step - Create trace matrix panel
        cy.clickButtonWithName("Create trace matrix");

        // Step - Able to generate Trace Links and continue
        cy.clickButtonWithName("Generate Trace Links");
      });
    });
  });

  describe.only("Project Tim Preview", () => {
    it("displays artifact types on the graph", () => {
      // Step - Inputs Project name and description
      cy.setProjectIdentifier("standard");

      // Step - creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - creates Trace Matrix, just type the types of artifact
      cy.createTraceMatrix("requirement", "hazard");

      // Step - Uploads trace link files
      cy.uploadingTraceLinks(simpleProjectFilesMap.requirement2hazard);

      // Step - Checks that correct artifacts are displayed in the Tim Tree
      cy.contains("Hazard");
      cy.contains("Requirement");
    });

    it("displays trace links between artifact types on the graph", () => {
      // Step - Inputs Project name and description
      cy.setProjectIdentifier("standard");

      // Step - creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - creates Trace Matrix, just type the types of artifact
      cy.createTraceMatrix("requirement", "hazard");

      // Step - Uploads trace link files
      cy.uploadingTraceLinks(simpleProjectFilesMap.requirement2hazard);

      // Step - Checks the displayed Trace Links between artifacts
      cy.contains("5");
    });
    it("displays all nodes on the graph within the current view", () => {
      // Step - Inputs Project name and description
      cy.setProjectIdentifier("standard");

      // Step - creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - creates Trace Matrix, just type the types of artifact
      cy.createTraceMatrix("requirement", "hazard");

      // Step - Uploads trace link files
      cy.uploadingTraceLinks(simpleProjectFilesMap.requirement2hazard);

      // Step - Checks that there are the correct number of nodes within each artifact
      cy.contains("5 Nodes");
      cy.contains("5 Nodes");
    });
    it("displays the correct count of artifacts and links", () => {
      // Step - Inputs Project name and description
      cy.setProjectIdentifier("standard");

      // Step - creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - creates Trace Matrix, just type the types of artifact
      cy.createTraceMatrix("requirement", "hazard");

      // Step - Uploads trace link files
      cy.uploadingTraceLinks(simpleProjectFilesMap.requirement2hazard);

      // Step - Checks for display of Artifacts, Nodes and Trace Links within the Tim Tree
      cy.contains("hazard");
      cy.contains("Requirement");
      cy.contains("5");
      cy.contains("5 nodes");
    });
  });
  describe("I can manuualy create a Project", () => {
    it("can create a project with valid data", () => {
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
      cy.contains("5 nodes");

      // Step - Finalizes project by creating it
      cy.clickButtonWithName("Create Project");
    });
  });
});
