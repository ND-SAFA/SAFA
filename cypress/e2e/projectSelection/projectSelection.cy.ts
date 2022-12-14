import { DataCy, simpleProjectFiles, testProject } from "../../fixtures";
import { validUser } from "../../fixtures/data/user.json";

describe("Project Selection", () => {
  beforeEach(() => {
    cy.viewport(1024, 768);
    cy.dbResetProjects().loadNewProject();

    cy.visit("/open")
      .login(validUser.email, validUser.password)
      .location("pathname", { timeout: 5000 })
      .should("equal", "/open")
      .openProjectSelector();
  });

  describe("Project List", () => {
    describe("I can reload my list of projects", () => {
      it("Shows the list of projects", () => {
        cy.withinTableRows(DataCy.selectionProjectList, (tr) =>
          tr.should("have.length.above", 1)
        );
      });

      it("Reloads the list of projects", () => {
        cy.clickButton(DataCy.selectionReload, "first");

        cy.withinTableRows(DataCy.selectionProjectList, (tr) =>
          tr.should("have.length.above", 1)
        );
      });
    });

    describe("I can search for projects by name", () => {
      it("Filters for projects that match my search", () => {
        cy.inputText(DataCy.selectionSearch, testProject.name);

        cy.withinTableRows(DataCy.selectionProjectList, (tr) =>
          tr.should("contain.text", testProject.name)
        );
      });

      it("Displays no projects when none match", () => {
        cy.inputText(DataCy.selectionSearch, "$".repeat(20));

        cy.withinTableRows(DataCy.selectionProjectList, (tr) => {
          tr.should("have.length", 2);
        });
      });
    });

    describe("I can select a project to see its versions", () => {
      it("Selects a project and continues to the version step", () => {
        cy.withinTableRows(DataCy.selectionProjectList, (tr) => {
          tr.get(".v-simple-checkbox").first().click().click();
        });

        cy.getCy(DataCy.stepperBackButton).should("not.be.disabled");
      });

      it("Cannot continue without a project selected", () => {
        cy.withinTableRows(DataCy.selectionProjectList, (tr) => {
          tr.get(".v-simple-checkbox").first().click();
        });

        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
      });
    });
  });

  describe("Project CRUD", () => {
    describe("As an admin, I can edit a project's name and description", () => {
      it("edits a project", () => {
        cy.clickButton(DataCy.selectorEditButton, "first");

        cy.getCy(DataCy.projectEditModal).within(() =>
          cy
            .getCy(DataCy.projectEditNameInput)
            .type(" Edited")
            .clickButton(DataCy.projectEditSaveButton)
        );

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      });
    });

    describe("As an owner, I can delete a project", () => {
      it("Deletes a project", () => {
        cy.clickButton(DataCy.selectorDeleteButton, "first");

        cy.getCy(DataCy.projectDeleteModal).within(() => {
          cy.getCy(DataCy.modalTitle)
            .invoke("text")
            .then(() =>
              cy.inputText(DataCy.projectDeleteNameInput, testProject.name)
            );

          cy.clickButton(DataCy.projectDeleteConfirmButton);
        });

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      });
    });
  });

  describe("Project Version List", () => {
    describe("I can reload my list of project versions", () => {
      it("Displays project versions", () => {
        cy.projectSelectorContinue();

        cy.withinTableRows(DataCy.selectionVersionList, (tr) =>
          tr.should("have.length.above", 1)
        );
      });

      it("Reloads project versions", () => {
        cy.projectSelectorContinue();

        cy.clickButton(DataCy.selectionReload, "last");

        cy.withinTableRows(DataCy.selectionVersionList, (tr) =>
          tr.should("have.length.above", 1)
        );
      });
    });

    describe("I can select and load a version of the project", () => {
      it("Selects and loads a project and version", () => {
        cy.projectSelectorContinue().projectSelectorContinue();

        cy.getCy(DataCy.appLoading).should("be.visible");
      });

      it("Cannot continue if a version is not selected", () => {
        cy.projectSelectorContinue();

        cy.withinTableRows(DataCy.selectionVersionList, (tr) => {
          tr.get(".v-simple-checkbox").first().click();
        });

        cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
      });
    });
  });

  describe("Project Version CRUD", () => {
    describe("I can create a new major, minor, or revision version", () => {
      it("Can create a new major version", () => {
        cy.projectSelectorContinue().createNewVersion("major");

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      });

      it("Can create a new minor version", () => {
        cy.projectSelectorContinue().createNewVersion("minor");

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      });

      it("Can create a new revision version", () => {
        cy.projectSelectorContinue().createNewVersion("revision");

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      });
    });

    describe("I can delete a project version", () => {
      it("Deletes a version", () => {
        cy.projectSelectorContinue().createNewVersion("revision");

        cy.getCy(DataCy.selectionVersionList).within(() => {
          cy.clickButton(DataCy.selectorDeleteButton);
        });
        cy.getCy(DataCy.versionDeleteModal).within(() => {
          cy.clickButton(DataCy.versionDeleteConfirmButton);
        });

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      });
    });

    describe("I can upload new flat files to a project version", () => {
      it("Uploads files to the current version", () => {
        cy.projectSelectorContinue()
          .projectSelectorContinue()
          .openUploadFiles();

        cy.uploadFiles(
          DataCy.versionUploadFilesInput,
          ...simpleProjectFiles
        ).clickButton(DataCy.versionUploadFilesButton);

        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      });
    });

    // describe("[WIP] I can upload flat files to the current document");
  });
});
