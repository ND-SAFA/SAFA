import { SimpleProjectFilesMap } from "../fixtures/simpleProjectFilesMap";
import { validUser } from "../fixtures/user.json";

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
        cy.getCy("input-project-description")
          .last()
          .type("Safety Artifact Forest Analysis");

        cy.getCy("generic-stepper-continue").should("be.disabled");
      });

      it("can continue with a name set", () => {
        cy.setProjectInformationInStandardUpload(
          "SAFA",
          "Safety Artifact Forest Analysis"
        );

        cy.getCy("generic-stepper-continue").should("not.be.disabled");
      });
    });

    describe("I can Create sets of artifacts by type", () => {
      it("cannot create a new panel with an empty name", () => {
        cy.setProjectInformationInStandardUpload(
          "SAFA",
          "Safety Artifact Forest Analysis"
        );
        cy.getCy("generic-stepper-continue").should("not.be.disabled");
        cy.clickButton("generic-stepper-continue");

        cy.getCy("button-create-panel").should("not.be.disabled");
        cy.clickButton("button-create-panel");
        cy.getCy("button-create-panel").should("be.disabled");
      });

      it("Can create a new panel of artifacts", () => {
        cy.setProjectInformationInStandardUpload(
          "SAFA",
          "Safety Artifact Forest Analysis"
        );
        cy.getCy("generic-stepper-continue").should("not.be.disabled");
        cy.clickButton("generic-stepper-continue");

        cy.clickButton("button-create-panel");
        cy.getCy("input-artifact-type").last().type("Hazards");
        cy.clickButton("button-artifact-type");
        cy.uploadFiles("input-files", SimpleProjectFilesMap.hazard);
        //need to make new function to enter in all of the files left
      });
    });
    describe("I can delete artifacts", () => {
      it("can delete artifacts", () => {
        cy.setProjectInformationInStandardUpload(
          "SAFA",
          "Safety Artifact Forest Analysis"
        );
        cy.getCy("generic-stepper-continue").should("not.be.disabled");
        cy.clickButton("generic-stepper-continue");

        cy.clickButton("button-create-panel");
        cy.getCy("input-artifact-type").last().type("Hazards");
        cy.clickButton("button-artifact-type");
        cy.uploadFiles("input-files", SimpleProjectFilesMap.hazard);

        cy.clickButton("button-artifact-dropbox");
        cy.clickButton("button-delete-artifact");
      });
      it("cannot continue after deleted", () => {
        cy.setProjectInformationInStandardUpload(
          "SAFA",
          "Safety Artifact Forest Analysis"
        );
        cy.getCy("generic-stepper-continue").should("not.be.disabled");
        cy.clickButton("generic-stepper-continue");
        cy.clickButton("button-create-panel");
        cy.getCy("input-artifact-type").last().type("Hazards");
        cy.clickButton("button-artifact-type");
        cy.uploadFiles("input-files", SimpleProjectFilesMap.hazard);
        cy.clickButton("button-artifact-dropbox");
        cy.clickButton("button-delete-artifact");

        cy.getCy("generic-stepper-continue").should("be.disabled");
      });
    });

    describe("I can preview the list of artifacts loaded from a file", () => {
      it("displays buttons for all of the artifacts in the file", () => {
        cy.setProjectInformationInStandardUpload(
          "SAFA",
          "Safety Artifact Forest Analysis"
        );
        cy.getCy("generic-stepper-continue").should("not.be.disabled");
        cy.clickButton("generic-stepper-continue");
        cy.clickButton("button-create-panel");
        cy.getCy("input-artifact-type").last().type("Hazards");
        cy.clickButton("button-artifact-type");
        cy.uploadFiles("input-files", SimpleProjectFilesMap.hazard);

        cy.clickButton("button-artifact-dropbox");
        cy.clickButton("button-file-entities");
      });
    });

    describe("I can upload a file containing the artifacts I want to create", () => {
      it("cannot create a project without atleast one artifact", () => {
        cy.setProjectInformationInStandardUpload(
          "SAFA",
          "Safety Artifact Forest Analysis"
        );
        cy.getCy("generic-stepper-continue").should("not.be.disabled");
        cy.clickButton("generic-stepper-continue");

        cy.clickButton("button-create-panel");
        cy.getCy("button-create-panel").should("be.disabled");
        cy.getCy("generic-stepper-continue").should("be.disabled");
      });
      it("can continue after uploading artifacts", () => {
        cy.setProjectInformationInStandardUpload(
          "SAFA",
          "Safety Artifact Forest Analysis"
        );
        cy.getCy("generic-stepper-continue").should("not.be.disabled");
        cy.clickButton("generic-stepper-continue");

        cy.clickButton("button-create-panel");
        cy.getCy("input-artifact-type").last().type("Hazards");
        cy.clickButton("button-artifact-type");
        cy.uploadFiles("input-files", SimpleProjectFilesMap.hazard);

        cy.getCy("generic-stepper-continue").should("not.be.disabled");
        cy.clickButton("generic-stepper-continue");
      });
      it("can continue with bad file if errors are ignored", () => {
        cy.setProjectInformationInStandardUpload(
          "SAFA",
          "Safety Artifact Forest Analysis"
        );
        cy.getCy("generic-stepper-continue").should("not.be.disabled");
        cy.clickButton("generic-stepper-continue");

        cy.clickButton("button-create-panel");
        cy.getCy("input-artifact-type").last().type("requirement");
        cy.clickButton("button-artifact-type");
        cy.uploadFiles("input-files", SimpleProjectFilesMap.requirement2hazard);

        cy.getCy("generic-stepper-continue").should("be.disabled");
        cy.clickButton("button-ignore-errors"); //button hasnt been tested
      });
    });
  });

  describe("Project Trace Link Uploading", () => {
    describe("I can create sets of trace links between two artifacts", () => {
      it.only("can create a new panel of trace links", () => {
        cy.setProjectInformationInStandardUpload(
          "SAFA",
          "Safety Artifact Forest Analysis"
        );
        cy.getCy("generic-stepper-continue").should("not.be.disabled");
        cy.clickButton("generic-stepper-continue");

        cy.clickButton("button-create-panel");
        cy.getCy("input-artifact-type").last().type("hazard");
        cy.clickButton("button-artifact-type");
        cy.uploadFiles("input-files", SimpleProjectFilesMap.hazard);
        //cy.getCy("generic-stepper-continue").should("not.be.disabled"); //need to make error command function
        //if(cy.getCy("generic-stepper-continue").is("disabled")).clickButton("button-ignore-errors")
        // cy.clickButton("button-ignore-errors");

        cy.clickButton("button-create-panel");
        cy.getCy("input-artifact-type").last().type("Hazard2Hazard");
        cy.clickButton("button-artifact-type");
        cy.uploadFiles("input-files", SimpleProjectFilesMap.hazard2hazard);
        //cy.getCy("generic-stepper-continue").should("be.disabled");
        cy.clickButton("button-ignore-errors");

        //ANYTHING UNDER IS NEW CODE
        cy.clickButton("generic-stepper-continue");
        cy.clickButton("button-new-create-trace-matrix"); //
        cy.clickButton("button-select-source"); //
        cy.clickButton("haz");
        cy.clickButton("button-select-target");
        cy.clickButton("haz2haz");

        cy.clickButton("create-trace-matrix"); //
        cy.uploadFiles("input-files", SimpleProjectFilesMap.hazard2hazard);
        cy.clickButton("generate-trace-links"); //

        cy.getCy("button-new-create-trace-matrix").should("not.be.disabled"); //
        cy.clickButton("button-new-create-trace-matrix"); //
      });
      it("cannot create a new panel withoutselecting two artifact types", () => {});
    });
  });
});
