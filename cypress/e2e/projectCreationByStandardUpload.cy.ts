/* eslint-disable max-lines */
import {
  DataCy,
  simpleProjectFilesMap,
  testFileMap,
  testProject,
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
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);

        cy.getCy(DataCy.creationCreatePanelButton).should("not.be.disabled");
        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.getCy(DataCy.creationCreatePanelButton).should("be.disabled");
      });

      it("Can create a new panel of artifacts", () => {
        cy.setProjectIdentifier("standard");
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);

        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "Hazards");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard
        );
        //need to make new function to enter in all of the files left
      });
    });
    describe("I can delete artifacts", () => {
      it("can delete artifacts", () => {
        cy.setProjectIdentifier("standard");
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);

        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "Hazards");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard
        );

        cy.clickButton(DataCy.creationArtifactButton);
        cy.clickButton(DataCy.creationArtifactDeleteButton);
      });
      it("cannot continue after deleted", () => {
        cy.setProjectIdentifier("standard");
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);
        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "Hazards");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard
        );
        cy.clickButton(DataCy.creationArtifactButton);
        cy.clickButton(DataCy.creationArtifactDeleteButton);

        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
      });
    });

    describe("I can preview the list of artifacts loaded from a file", () => {
      it("displays buttons for all of the artifacts in the file", () => {
        cy.setProjectIdentifier("standard");
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);
        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "Hazards");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard
        );

        cy.clickButton(DataCy.creationArtifactButton);
        cy.clickButton(DataCy.creationEntitiesButton);
      });
    });

    describe("I can upload a file containing the artifacts I want to create", () => {
      it("can continue after uploading artifacts", () => {
        cy.setProjectIdentifier("standard");
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);

        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "Hazards");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard
        );

        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);
      });
      it("can continue with bad file if errors are ignored", () => {
        cy.setProjectIdentifier("standard");
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);

        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "requirement");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.requirement2hazard
        );

        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
        cy.clickButton(DataCy.creationIgnoreErrorsButton, undefined); //button hasnt been tested
      });
    });
  });

  describe("Project Trace Link Uploading", () => {
    describe("I can create sets of trace links between two artifacts", () => {
      it("can create a new panel of trace links", () => {
        cy.setProjectIdentifier("standard");
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);

        // Step - Create hazard panel and upload file
        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "hazard");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard
        );

        // Step - Create invalid artifact type (Hazard2Hazard)
        cy.clickButton(DataCy.creationCreatePanelButton);

        cy.inputText(DataCy.creationTypeInput, "Hazard2Hazard");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard2hazard
        );

        // Step - wait 500ms (.5 sec) for app to parse file and gather errors
        cy.wait(500);

        // VP - Verify that continue button is disabled (file panel has errors)
        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");

        // Step - Ignore errors in hazard2hazard
        cy.clickButton(DataCy.creationIgnoreErrorsButton, "last");

        // Step - Move to step 3 (creating trace panels)
        cy.clickButton(DataCy.stepperContinueButton);

        // Step - Create new trace matrix
        cy.clickButtonWithName("Create new trace matrix");

        // Step - Select source artifact as "hazard"
        cy.clickButtonWithName("Select Source");
        cy.clickMenuOption("hazard");

        // Step - Select target artifact as "hazard"
        cy.clickButtonWithName("Select Target");
        cy.clickMenuOption("hazard");

        // Step - Create trace matrix panel
        cy.clickButtonWithName("Create trace matrix");

        // Step - uploads hazard2hazard file
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard2hazard
        );

        // Step - create a new panel
        cy.clickButtonWithName("Create new trace matrix");
      });
    });

    describe("I can delete a set of trace links", () => {
      it("can delete a set of trace links", () => {
        cy.setProjectIdentifier("standard");
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);

        // Step - Create requirement panel and upload file
        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "Requirement");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.requirement
        );

        cy.clickButton(DataCy.creationCreatePanelButton);

        //Step - create hazard panel and upload file
        cy.inputText(DataCy.creationTypeInput, "hazard");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard
        );

        // Step - wait 500ms (.5 sec) for app to parse file and gather errors
        cy.wait(500);

        // Step - Move to step 3 (creating trace panels)
        cy.clickButton("generic-stepper-continue");

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

        // Step - being able to delete a set of trace links
        cy.clickButton("button-delete-artifact", "last");
      });
    });

    describe("I can preview the list of trace links loaded from a file", () => {
      it("displays buttons for all of the trace links in the file", () => {
        cy.setProjectIdentifier("standard");
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);

        // Step - Create requirement panel and upload file
        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "Requirement");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.requirement
        );

        cy.clickButton(DataCy.creationCreatePanelButton);

        //Step - create hazard panel and upload file
        cy.inputText(DataCy.creationTypeInput, "hazard");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard
        );
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

    describe("I can upload a file containing the trace links I want to create", () => {
      it("can continue with no trace links", () => {
        cy.setProjectIdentifier("standard");
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);

        // Step - Create requirement panel and upload file
        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "Empty design");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          testFileMap.Emptydesign
        );

        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "Empty design2design");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          testFileMap.Emptydesign2design
        );

        cy.clickButton(DataCy.creationIgnoreErrorsButton, "last");

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
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);

        // Step - Create requirement panel and upload file
        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "Requirement");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.requirement
        );

        cy.clickButton(DataCy.creationCreatePanelButton);

        //Step - create hazard panel and upload file
        cy.inputText(DataCy.creationTypeInput, "hazard");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard
        );

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
      });

      it("can continue with a bad file if errors are ignored", () => {
        cy.setProjectIdentifier("standard");
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);

        // Step - Create hazard panel and upload file
        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "hazard");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard
        );

        cy.clickButton(DataCy.creationCreatePanelButton);

        //Step - create hazard2hazard panel and upload file
        cy.inputText(DataCy.creationTypeInput, "hazard2hazard");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard2hazard
        );

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
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);

        // Step - Create requirement panel and upload file
        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.inputText(DataCy.creationTypeInput, "Requirement");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.requirement
        );

        cy.clickButton(DataCy.creationCreatePanelButton);

        //Step - create hazard panel and upload file
        cy.inputText(DataCy.creationTypeInput, "hazard");
        cy.clickButton(DataCy.creationTypeButton);
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard
        );
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

        // Step - Able to generate Trace Links and continue
        cy.clickButtonWithName("Generate Trace Links");
        cy.clickButton(DataCy.stepperContinueButton);
      });
    });
  });
  describe("Project Tim Preview", () => {
    it("displays artifact types on the graph", () => {});
    it("displays trace links between artifact types on the graph", () => {});
    it("displays the correct count of artifacts and links", () => {});
  });
});
