import {
  DataCy,
  Routes,
  simpleProjectFilesMap,
  testFileMap,
  testProject,
} from "@/fixtures";

const validUser = Cypress.env("validUser");

describe.skip("Standard Project Creation", () => {
  beforeEach(() => {
    cy.dbResetJobs().dbResetProjects();

    cy.loginToPage(validUser.email, validUser.password, Routes.PROJECT_CREATOR);
  });

  describe("Project Artifact Uploading", () => {
    it("Cannot create a project without a name", () => {
      cy.inputText(
        DataCy.creationStandardDescriptionInput,
        testProject.description
      );

      cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
    });

    describe("I can create sets of artifacts by type", () => {
      it("Cannot create a new panel with an empty name", () => {
        // Step - Inputs Project name and description
        cy.setProjectIdentifier("standard");

        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
      });

      it("Can create a new panel of artifacts", () => {
        cy.setProjectIdentifier("standard").createArtifactPanel(
          "hazard",
          simpleProjectFilesMap.hazard
        );

        cy.getCy(DataCy.creationFilePanel).should("be.visible");
      });
    });

    describe("I can delete artifacts", () => {
      it("Can delete artifacts", () => {
        cy.setProjectIdentifier("standard").createArtifactPanel(
          "hazard",
          simpleProjectFilesMap.hazard
        );

        cy.openPanelAfterClose().clickButton(
          DataCy.creationArtifactDeleteButton,
          "first",
          true
        );

        cy.getCy(DataCy.creationFilePanel).should("not.exist");
      });
    });

    describe("I can preview the list of artifacts loaded from a file", () => {
      it("Displays buttons for all of the artifacts in the file", () => {
        cy.setProjectIdentifier("standard").createArtifactPanel(
          "hazard",
          simpleProjectFilesMap.hazard
        );

        cy.getCy(DataCy.creationDeletePanel).should("not.be.visible");

        cy.openPanelAfterClose()
          .clickButtonWithName("Parsed Entities")
          .getCy(DataCy.creationEntitiesButton)
          .should("have.length", 5);
      });
    });

    describe("I can upload a file containing the artifacts I want to create", () => {
      it("Can continue after uploading artifacts", () => {
        cy.setProjectIdentifier("standard").createArtifactPanel(
          "hazard",
          simpleProjectFilesMap.hazard
        );

        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
      });

      it("Can continue with bad file if errors are ignored", () => {
        cy.setProjectIdentifier("standard").createArtifactPanel(
          "requirement",
          simpleProjectFilesMap.requirement2requirement
        );

        cy.clickButton(DataCy.creationIgnoreErrorsButton, undefined);

        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
      });
    });
  });

  describe("Project Trace Link Uploading", () => {
    describe("I can create sets of trace links between two artifact types", () => {
      it("Can create a new panel of trace links", () => {
        cy.createReqToHazardFiles().createTraceMatrix("requirement", "hazard");

        cy.getCy(DataCy.creationFilePanel).should("be.visible");
      });

      it("Cannot create a new panel without selecting two artifact types", () => {
        cy.createReqToHazardFiles();

        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
      });
    });

    describe("I can delete a set of trace links", () => {
      it("Can delete a set of trace links", () => {
        cy.createReqToHazardFiles(true);

        cy.getCy(DataCy.creationDeletePanel)
          .should("not.be.visible")
          .openPanelAfterClose();
        cy.clickButton(DataCy.creationDeletePanel);

        cy.contains("requirement to hazard").should("not.exist");
      });
    });

    describe("I can preview the list of trace links loaded from a file", () => {
      it("Displays buttons for all of the trace links in the file", () => {
        cy.createReqToHazardFiles(true);

        cy.getCy(DataCy.creationDeletePanel).should("not.be.visible");

        cy.openPanelAfterClose()
          .clickButtonWithName("Parsed Entities")
          .getCy(DataCy.creationEntitiesButton)
          .should("have.length", 5);
      });
    });

    describe("I can upload a file containing the trace links I want to create", () => {
      it("Can continue with no trace links", () => {
        cy.setProjectIdentifier("standard");

        cy.createArtifactPanel(
          "Empty Design",
          testFileMap.emptyDesign2Design
        ).clickButton(DataCy.creationIgnoreErrorsButton, undefined);

        cy.createArtifactPanel("Empty design", testFileMap.emptyDesign, true);

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
        cy.createReqToHazardFiles().createTraceMatrix("hazard", "requirement");

        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");

        cy.uploadFiles(
          DataCy.creationStandardFilesInput,
          simpleProjectFilesMap.tim
        );

        cy.clickButton(DataCy.creationIgnoreErrorsButton, "last");

        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
      });
    });

    describe("I can generate trace links between artifacts", () => {
      it("Can continue with trace links set to be generated", () => {
        cy.createReqToHazardFiles().createTraceMatrix("requirement", "hazard");

        cy.openPanelAfterClose();

        cy.clickButtonWithName("Generate Trace Links");

        cy.getCy(DataCy.stepperContinueButton).should("not.be.disabled");
      });
    });
  });

  describe.skip("TIM Preview", () => {
    describe("I can view the TIM of a project being created", () => {
      it("Displays all nodes on the graph", () => {
        cy.createReqToHazardFiles(true, true);

        cy.getCy("tim-node")
          .should("be.visible")
          .within(() => {
            cy.contains("requirement").should("be.visible");
            cy.contains("hazard").should("be.visible");
            cy.contains("5 Nodes").should("be.visible");
          });
      });
    });
  });

  describe("I can manually create a Project", () => {
    it("Can create a project with valid data", () => {
      cy.createReqToHazardFiles(true, true).clickButton(
        DataCy.stepperContinueButton
      );

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.waitForJobLoad();
    });
  });
});
