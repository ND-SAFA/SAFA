import { SimpleProjectFilesMap } from "../fixtures/simpleProjectFilesMap";
import { validUser } from "../fixtures/user.json";

describe("Project Creation", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080/create").login(
      validUser.email,
      validUser.password
    );
  });

  describe("Manual Project Creation", () => {
    describe("Project Artifact Uploading", () => {
      it("cant continue without name", () => {
        cy.getCy("input-project-description")
          .last()
          .type("Safety Artifact Forest Analysis");

        cy.getCy("generic-stepper-continue").should("be.disabled");
      });

      it("cant continue without description", () => {
        cy.getCy("input-project-name").last().type("SAFA");

        cy.getCy("generic-stepper-continue").should("be.disabled");
      });

      it("can create a valid project", () => {
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
        cy.clickButton("button-file-entities"); //code doesnt - work entities button
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
        cy.clickButton("button-ignore-errors");
      });
    });
  });
});
