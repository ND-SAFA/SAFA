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
    describe("I can manually create a project", () => {
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

      it("can create artifacts", () => {
        cy.setProjectInformationInStandardUpload(
          "SAFA",
          "Safety Artifact Forest Analysis"
        );
        cy.getCy("generic-stepper-continue").should("not.be.disabled");
        cy.clickButton("generic-stepper-continue");

        cy.clickButton("button-artifact-type");
        cy.getCy("input-artifact-type").last().type("Hazards");
        cy.clickButton("button-artifact-type");
      });

      //it("cant upload artifacts",() => {
      //visual effects i haved learned (requirements artifacts)
      //visual effects i haved learned (X next to title )
      //cy.getCy("generic-stepper-continue").should("not.be.disabled");
      //});

      it("can upload ", () => {
        cy.getCy("input-project-name").last().type("SAFA");
        cy.getCy("input-project-description")
          .last()
          .type("Safety Artifact Forest Analysis");
        cy.getCy("generic-stepper-continue").should("not.be.disabled");
        cy.clickButton("generic-stepper-continue");
        cy.clickButton("create-new-artifact-button");
        cy.getCy("input-artifact-name").last().type("Hazards");
        cy.clickButton("create-artifact-button");

        cy.clickButton("Upload-Files");
        cy.uploadFiles("input-files", SimpleProjectFilesMap.hazard);
      });
    });
  });
});
