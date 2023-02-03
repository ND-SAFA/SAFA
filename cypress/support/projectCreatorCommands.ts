import {
  DataCy,
  miniProjectFiles,
  Routes,
  simpleProjectFilesMap,
  testProject,
  validUser,
} from "@/fixtures";

Cypress.Commands.add("initEmptyProject", () => {
  cy.dbResetJobs().dbResetProjects();

  cy.visit(Routes.PROJECT_CREATOR + "?tab=bulk")
    .login(validUser.email, validUser.password)
    .locationShouldEqual(Routes.PROJECT_CREATOR);

  cy.setProjectIdentifier("bulk")
    .clickButton(DataCy.creationEmptyToggle)
    .clickButton(DataCy.creationUploadButton);
});

Cypress.Commands.add("initProject", (waitForComplete = true) => {
  cy.dbResetJobs().dbResetProjects();

  cy.visit(Routes.PROJECT_CREATOR + "?tab=bulk")
    .login(validUser.email, validUser.password)
    .locationShouldEqual(Routes.PROJECT_CREATOR);

  cy.setProjectIdentifier("bulk")
    .uploadFiles(DataCy.creationBulkFilesInput, ...miniProjectFiles)
    .clickButton(DataCy.creationUploadButton);

  if (!waitForComplete) return;

  cy.waitForJobLoad();
});

Cypress.Commands.add("initProjectVersion", (waitForComplete = true) => {
  cy.dbResetVersions();

  cy.visit(Routes.MY_PROJECTS)
    .login(validUser.email, validUser.password)
    .locationShouldEqual(Routes.MY_PROJECTS);

  cy.expandViewport()
    .projectSelectorContinue("project")
    .projectSelectorContinue("version")
    .locationShouldEqual(Routes.ARTIFACT);

  cy.waitForProjectLoad(waitForComplete);
});

Cypress.Commands.add("setProjectIdentifier", (type) => {
  if (type === "standard") {
    cy.getCy(DataCy.creationStandardNameInput).type(testProject.name);
    cy.getCy(DataCy.creationStandardDescriptionInput).type(
      testProject.description
    );
    cy.clickButton(DataCy.stepperContinueButton);
  } else if (type === "modal") {
    cy.getCy(DataCy.projectEditNameInput).type(testProject.name);
    cy.getCy(DataCy.projectEditDescriptionInput).type(testProject.description);
  } else {
    cy.getCy(DataCy.creationBulkNameInput).type(testProject.name);
    cy.getCy(DataCy.creationBulkDescriptionInput).type(testProject.description);
  }
});

Cypress.Commands.add("openPanelAfterClose", () => {
  // Wait is required for waiting until the close animation completes.
  cy.wait(200).clickButton(DataCy.creationFilePanel, "last");
});

Cypress.Commands.add("createArtifactPanel", (name, file, next) => {
  cy.clickButton(DataCy.creationCreatePanelButton);
  cy.getCy(DataCy.creationTypeInput).type(name);
  cy.clickButton(DataCy.creationTypeButton);
  cy.uploadFiles(DataCy.creationStandardFilesInput, file);

  if (next) {
    cy.clickButton(DataCy.stepperContinueButton);
  }
});

Cypress.Commands.add("createTraceMatrix", (source, target, file, next) => {
  cy.clickButtonWithName("Create new trace matrix")
    .clickSelectOption(DataCy.creationTraceSourceInput, source)
    .clickSelectOption(DataCy.creationTraceTargetInput, target)
    .clickButton(DataCy.creationTraceCreateButton);

  if (file) {
    cy.uploadFiles(DataCy.creationStandardFilesInput, file);
  }

  if (next) {
    cy.clickButton(DataCy.stepperContinueButton);
  }
});

Cypress.Commands.add("createReqToHazardFiles", (createTraces, next) => {
  cy.setProjectIdentifier("standard");
  cy.createArtifactPanel("requirement", simpleProjectFilesMap.requirement);
  cy.createArtifactPanel("hazard", simpleProjectFilesMap.hazard, true);

  if (createTraces) {
    cy.createTraceMatrix(
      "requirement",
      "hazard",
      simpleProjectFilesMap.requirement2hazard,
      next
    );
  }
});

Cypress.Commands.add("waitForJobLoad", () => {
  cy.wrap(null, { timeout: 10000 }).then(() => {
    cy.getCy(DataCy.jobStatus, "first", 10000).should(
      "contain.text",
      "Completed"
    );
  });
});

// Cypress.Commands.add("loadProject", () => {
//   cy.visit("/create")
//     .login(validUser.email, validUser.password)
//     .location("pathname", { timeout: 5000 })
//     .should("equal", "/create");
//
//   cy.intercept({ method: "POST", url: "/projects" }).as("postProject");
//
//   cy.switchTab("Bulk Upload")
//     .setProjectIdentifier("bulk")
//     .uploadFiles(DataCy.creationBulkFilesInput, ...miniProjectFiles)
//     .clickButton(DataCy.creationUploadButton);
//
//   cy.wait("@postProject").then((interception) => {
//     const { body } = interception.response;
//     const versionId = body.projectVersion.versionId;
//
//     cy.wrap(null, { timeout: 10000 }).then(() => {
//       cy.streamRequest<any>(
//         {
//           url: `wss://dev-api.safa.ai`,
//         },
//         {}
//       ).then((results) => {
//         const result = results?.[1];
//         const data = result?.data;
//       });
//     });
//   });
//
//   cy.getCy(DataCy.jobStatus, "first", 20000).should(
//     "contain.text",
//     "Completed"
//   );
// });
