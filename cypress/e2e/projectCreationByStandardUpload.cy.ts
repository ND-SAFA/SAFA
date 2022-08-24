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

  afterEach(() => {
    cy.logout();
  });

  describe("Manual Project Creation", () => {
    describe("Project Artifact Uploading", () => {
      it("cant continue without name", () => {
        cy.inputText(
          DataCy.creationStandardDescriptionInput,
          testProject.description
        );

        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
      });

      it("can continue with a name set", () => {
        cy.setProjectIdentifier("standard");

        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
      });
    });

    describe("I can Create sets of artifacts by type", () => {
      it("cannot create a new panel with an empty name", () => {
        cy.setProjectIdentifier("standard");

        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.wait(500);
        cy.getCy(DataCy.creationCreatePanelButton).should("be.disabled");
      });

      it("Can create a new panel of artifacts", () => {
        cy.setProjectIdentifier("standard");

        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);
      });
    });
    describe("I can delete artifacts", () => {
      it("can delete artifacts", () => {
        cy.setProjectIdentifier("standard");

        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - opens up artifact drop box and deletes artifact
        cy.clickButton(DataCy.creationArtifactButton);
        cy.clickButton(DataCy.creationArtifactDeleteButton);
      });
      it("cannot continue after deleted", () => {
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
        cy.setProjectIdentifier("standard");

        // Step - Created Hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        cy.clickButton(DataCy.creationArtifactButton);
        cy.clickButton(DataCy.creationEntitiesButton);
      });
    });

    describe("I can upload a file containing the artifacts I want to create", () => {
      it("can continue after uploading artifacts", () => {
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
      });
    });
  });

  describe("Project Trace Link Uploading", () => {
    describe("I can create sets of trace links between two artifact types", () => {
      it("can create a new panel of trace links", () => {
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Move to step 3 (creating trace panels)
        cy.clickButton(DataCy.stepperContinueButton);

        cy.clickButtonWithName("Create new trace matrix");
        // Step - Select source artifact as "hazard"
        cy.clickButtonWithName("Select Source");
        cy.clickMenuOption("requirement");

        // Step - Select target artifact as "hazard"
        cy.clickButtonWithName("Select Target");
        cy.clickMenuOption("hazard");

        // Step - Create trace matrix panel
        cy.clickButtonWithName("Create trace matrix");
      });
    });
    describe("I can delete a set of trace links", () => {
      it("can delete a set of trace links", () => {
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Move to step 3 (creating trace panels)
        cy.clickButton(DataCy.stepperContinueButton);

        cy.clickButtonWithName("Create new trace matrix");

        // Step - Select source artifact as "hazard"
        cy.clickButtonWithName("Select Source");
        cy.clickMenuOption("requirement");

        // Step - Select target artifact as "hazard"
        cy.clickButtonWithName("Select Target");
        cy.clickMenuOption("hazard");

        // Step - Create trace matrix panel
        cy.clickButtonWithName("Create trace matrix");

        // Step - being able to delete a set of trace links
        cy.clickButton("button-delete-artifact", "last");
      });
    });

    describe("I can preview the list of trace links loaded from a file", () => {
      it("displays buttons for all of the trace links in the file", () => {
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Move to step 3 (creating trace panels)
        cy.clickButton(DataCy.stepperContinueButton);

        cy.clickButtonWithName("Create new trace matrix");

        // Step - Select source artifact as "hazard"
        cy.clickButtonWithName("Select Source");
        cy.clickMenuOption("requirement");

        // Step - Select target artifact as "hazard"
        cy.clickButtonWithName("Select Target");
        cy.clickMenuOption("hazard");

        // Step - Create trace matrix panel
        cy.clickButtonWithName("Create trace matrix");

        // Step - uploads trace link files (Requirement2Hazard)
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.requirement2hazard
        );
        // Step - opening dropbox to check entities
        cy.clickButtonWithName("requirement-hazard");
        cy.wait(500);

        // Step - making sure entities are viewable
        cy.clickButton(DataCy.creationEntitiesButton, "last");
      });
    });
    // NEED THE BEFORE EACH TO STOP WORKING FOR THIS TEST DUE TO DIFFERENT ARTIFACTS USED ---------------------------------------------
    describe("I can upload a file containing the trace links I want to create", () => {
      it("can continue with no trace links", () => {
        cy.setProjectIdentifier("standard");
        //cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");

        cy.createArtifactPanel("Empty Design", testFileMap.Emptydesign2design);
        cy.clickButton(DataCy.creationIgnoreErrorsButton, undefined);

        cy.createArtifactPanel(
          "Design2design",
          simpleProjectFilesMap.design2design
        );

        cy.getCy(DataCy.creationIgnoreErrorsButton).click(); // IGNORE BUTTONS ISNT WORKING

        cy.wait(1000);
        // Step - Move to step 3 (creating trace panels)
        cy.clickButton(DataCy.stepperContinueButton);
        // Step - wait 500ms (.5 sec) for app to parse file and gather errors
        cy.wait(500);

        // Step - Move to step 3 (creating trace panels)
        cy.clickButton(DataCy.stepperContinueButton);

        // Step - Create new trace matrix
        cy.clickButtonWithName("Create new trace matrix");

        // Step - Select source artifact as "hazard"
        cy.clickButtonWithName("Select Source");
        cy.clickMenuOption("design");

        cy.clickButtonWithName("Select Target");
        cy.clickMenuOption("design");

        cy.clickButtonWithName("Create trace matrix");

        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          testFileMap.Emptydesign2design
        );

        cy.clickButton(DataCy.stepperContinueButton);
      });
      it("can continue after uploading trace links", () => {
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Move to step 3 (creating trace panels)
        cy.clickButton(DataCy.stepperContinueButton);

        // Step - wait 500ms (.5 sec) for app to parse file and gather errors
        cy.wait(500);

        // Step - Create new trace matrix
        cy.clickButtonWithName("Create new trace matrix");

        // Step - Select source artifact as "hazard"
        cy.clickButtonWithName("Select Source");
        cy.clickMenuOption("requirement");

        // Step - Select target artifact as "hazard"
        cy.clickButtonWithName("Select Target");
        cy.clickMenuOption("hazard");

        // Step - Create trace matrix panel
        cy.clickButtonWithName("Create trace matrix");

        //uploads trace link files (requirement2Hazard)
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.requirement2hazard
        );
        //Step - finalizes trace links and is able to continue with project TIM
        cy.clickButton(DataCy.stepperContinueButton);
      });

      it("can continue with a bad file if errors are ignored", () => {
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Move to step 3 (creating trace panels)
        cy.clickButton(DataCy.stepperContinueButton);

        cy.clickButton(DataCy.creationIgnoreErrorsButton, "last");

        cy.clickButton(DataCy.stepperContinueButton);

        cy.clickButtonWithName("Create new trace matrix");

        cy.clickButtonWithName("Select Source");
        cy.clickMenuOption("hazard");

        // Step - Select target artifact as "hazard"
        cy.clickButtonWithName("Select Target");
        cy.clickMenuOption("hazard2hazard");

        // Step - Create trace matrix panel
        cy.clickButtonWithName("Create trace matrix");

        //uploads trace link files (Hazard2Hazrd)
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard2hazard
        );
        //Step - being able to continue after ignoring errors from hazard2hazard errors
        cy.clickButton(DataCy.creationIgnoreErrorsButton, "last");
        cy.clickButton(DataCy.stepperContinueButton);
      });
    });
    describe("I can generate trace links between artifacts", () => {
      it("can continue with trace links set to be generated", () => {
        cy.setProjectIdentifier("standard");

        // Step - creates requirement artifact
        cy.createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement
        );

        // Step - creates hazard artifact
        cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

        // Step - Move to step 3 (creating trace panels)
        cy.clickButton(DataCy.stepperContinueButton);
        // Step - wait 500ms (.5 sec) for app to parse file and gather errors
        cy.wait(500);

        // Step - Create new trace matrix
        cy.clickButtonWithName("Create new trace matrix");

        // Step - Select source artifact as "hazard"
        cy.clickButtonWithName("Select Source");
        cy.clickMenuOption("requirement");

        // Step - Select target artifact as "hazard"
        cy.clickButtonWithName("Select Target");
        cy.clickMenuOption("hazard");

        // Step - Create trace matrix panel
        cy.clickButtonWithName("Create trace matrix");

        // Step - Able to generate Trace Links and continue
        cy.clickButtonWithName("Generate Trace Links");
        cy.clickButton(DataCy.stepperContinueButton);
      });
    });
  });
  describe("Project Tim Preview", () => {
    it("displays artifact types on the graph", () => {
      cy.setProjectIdentifier("standard");

      // Step - creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - Move to step 3 (creating trace panels)
      cy.clickButton(DataCy.stepperContinueButton);

      // Step - wait 500ms (.5 sec) for app to parse file and gather errors
      cy.wait(500);

      // Step - Move to step 3 (creating trace panels)
      cy.clickButton(DataCy.stepperContinueButton);

      // Step - Create new trace matrix
      cy.clickButtonWithName("Create new trace matrix");

      // Step - Select source artifact as "hazard"
      cy.clickButtonWithName("Select Source");
      cy.clickMenuOption("requirement");

      // Step - Select target artifact as "hazard"
      cy.clickButtonWithName("Select Target");
      cy.clickMenuOption("hazard");

      // Step - Create trace matrix panel
      cy.clickButtonWithName("Create trace matrix");

      //uploads trace link files (requirement2Hazard)
      cy.uploadFiles(
        DataCy.creationStandardFilesInput,
        simpleProjectFilesMap.requirement2hazard
      );
      //Step - finalizes trace links and is able to continue with project TIM
      cy.clickButton(DataCy.stepperContinueButton);

      cy.wait(3000);

      cy.contains("Hazard");
      cy.contains("Requirement");

      // NEED TO CREATE COMMAND TO CHECK BOTH REQUIREMENT AND HAZARD ARE INDEED ARTIFACTS ON THE TIM TREE ----------------------------------
    });
    it("displays trace links between artifact types on the graph", () => {
      cy.setProjectIdentifier("standard");

      // Step - creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - Move to step 3 (creating trace panels)
      cy.clickButton(DataCy.stepperContinueButton);

      // Step - wait 500ms (.5 sec) for app to parse file and gather errors
      cy.wait(500);

      // Step - Move to step 3 (creating trace panels)
      cy.clickButton(DataCy.stepperContinueButton);

      // Step - Create new trace matrix
      cy.clickButtonWithName("Create new trace matrix");

      // Step - Select source artifact as "hazard"
      cy.clickButtonWithName("Select Source");
      cy.clickMenuOption("requirement");

      // Step - Select target artifact as "hazard"
      cy.clickButtonWithName("Select Target");
      cy.clickMenuOption("hazard");

      // Step - Create trace matrix panel
      cy.clickButtonWithName("Create trace matrix");

      //uploads trace link files (requirement2Hazard)
      cy.uploadFiles(
        DataCy.creationStandardFilesInput,
        simpleProjectFilesMap.requirement2hazard
      );
      //Step - finalizes trace links and is able to continue with project TIM
      cy.clickButton(DataCy.stepperContinueButton);

      // NEED TO MAKE COMMAND TO CHECK THE AMOUNT OF LINKS ---------------------------------------------------------------------------

      cy.wait(1000);

      cy.contains("5");
    });
    it("displays all nodes on the graph within the current view", () => {
      cy.setProjectIdentifier("standard");

      // Step - creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - Move to step 3 (creating trace panels)
      cy.clickButton(DataCy.stepperContinueButton);

      // Step - wait 500ms (.5 sec) for app to parse file and gather errors
      cy.wait(500);

      // Step - Move to step 3 (creating trace panels)
      cy.clickButton(DataCy.stepperContinueButton);

      // Step - Create new trace matrix
      cy.clickButtonWithName("Create new trace matrix");

      // Step - Select source artifact as "hazard"
      cy.clickButtonWithName("Select Source");
      cy.clickMenuOption("requirement");

      // Step - Select target artifact as "hazard"
      cy.clickButtonWithName("Select Target");
      cy.clickMenuOption("hazard");

      // Step - Create trace matrix panel
      cy.clickButtonWithName("Create trace matrix");

      //uploads trace link files (requirement2Hazard)
      cy.uploadFiles(
        DataCy.creationStandardFilesInput,
        simpleProjectFilesMap.requirement2hazard
      );
      //Step - finalizes trace links and is able to continue with project TIM
      cy.clickButton(DataCy.stepperContinueButton);

      // NEED TO MAKE COMMAND WHERE IT CHECKS ALL THE CURRENT NODES ON THE GRAPH -------------------------------------------------------

      cy.contains("5 Nodes");
      cy.contains("5 Nodes");
    });
    it("displays the correct count of artifacts and links", () => {
      cy.setProjectIdentifier("standard");

      // Step - creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - Move to step 3 (creating trace panels)
      cy.clickButton(DataCy.stepperContinueButton);

      // Step - wait 500ms (.5 sec) for app to parse file and gather errors
      cy.wait(500);

      // Step - Move to step 3 (creating trace panels)
      cy.clickButton(DataCy.stepperContinueButton);

      // Step - Create new trace matrix
      cy.clickButtonWithName("Create new trace matrix");

      // Step - Select source artifact as "hazard"
      cy.clickButtonWithName("Select Source");
      cy.clickMenuOption("requirement");

      // Step - Select target artifact as "hazard"
      cy.clickButtonWithName("Select Target");
      cy.clickMenuOption("hazard");

      // Step - Create trace matrix panel
      cy.clickButtonWithName("Create trace matrix");

      //uploads trace link files (requirement2Hazard)
      cy.uploadFiles(
        DataCy.creationStandardFilesInput,
        simpleProjectFilesMap.requirement2hazard
      );
      //Step - finalizes trace links and is able to continue with project TIM
      cy.clickButton(DataCy.stepperContinueButton);

      // ADD COMMANDS FROM FIRST AND SECOND TESTS FROM THE PROJECT TIM PREVIEW ----------------------------------------------------
      cy.contains("hazard");
      cy.contains("Requirement");
      cy.contains("5");
      cy.contains("5 nodes");
    });
  });
  describe("I can manuualy create a Project", () => {
    it("can create a project with valid data", () => {
      cy.setProjectIdentifier("standard");

      // Step - creates requirement artifact
      cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);

      // Step - creates hazard artifact
      cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard);

      // Step - Move to step 3 (creating trace panels)
      cy.clickButton(DataCy.stepperContinueButton);

      // Step - wait 500ms (.5 sec) for app to parse file and gather errors
      cy.wait(500);

      // Step - Move to step 3 (creating trace panels)
      cy.clickButton(DataCy.stepperContinueButton);

      // Step - Create new trace matrix
      cy.clickButtonWithName("Create new trace matrix");

      // Step - Select source artifact as "hazard"
      cy.clickButtonWithName("Select Source");
      cy.clickMenuOption("requirement");

      // Step - Select target artifact as "hazard"
      cy.clickButtonWithName("Select Target");
      cy.clickMenuOption("hazard");

      // Step - Create trace matrix panel
      cy.clickButtonWithName("Create trace matrix");

      //uploads trace link files (requirement2Hazard)
      cy.uploadFiles(
        DataCy.creationStandardFilesInput,
        simpleProjectFilesMap.requirement2hazard
      );
      //Step - finalizes trace links and is able to continue with project TIM
      cy.clickButton(DataCy.stepperContinueButton);

      // STEP - checking artifacts
      // STEP - checking tracelinks
      // STEP - checking nodes
      // STEP -
      cy.clickButtonWithName("Create Project");

      cy.wait(1000);
      cy.contains("hazard");
      cy.contains("Requirement");
      cy.contains("5");
      cy.contains("5 nodes");
    });
  });
});
