import {
  DataCy,
  simpleProjectFilesMap,
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
      it("cannot create a project without atleast one artifact", () => {
        cy.setProjectIdentifier("standard");
        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
        cy.clickButton(DataCy.stepperContinueButton);

        cy.clickButton(DataCy.creationCreatePanelButton);
        cy.getCy(DataCy.creationCreatePanelButton).should("be.disabled");
        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
      });
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
      it.only("can create a new panel of trace links", () => {
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
        //cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled"); //need to make error command function
        //if(cy.getCy(DataCy.stepperContinueButton).is("disabled")).clickButton(DataCy.creationIgnoreErrorsButton, undefined)
        // cy.clickButton(DataCy.creationIgnoreErrorsButton, undefined);

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

        /**
         * WORK IN PROGRESS
         */

        cy.clickButton("create-trace-matrix"); // Add new DataCy option
        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.hazard2hazard
        );
        cy.clickButton("generate-trace-links"); // Add new DataCy option

        cy.getCy("button-new-create-trace-matrix").should("not.be.disabled"); // Add new DataCy option
        cy.clickButton("button-new-create-trace-matrix");
      });

      it("cannot create a new panel withoutselecting two artifact types", () => {});
    });
  });
});
