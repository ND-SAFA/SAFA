import { DataCy, testProject, validUser } from "../fixtures";

describe("Project Selection", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080")
      .login(validUser.email, validUser.password)
      .openProjectSelector();
  });

  afterEach(() => {
    cy.location().then((location) => {
      if (!location.href.includes("project")) {
        cy.closeModal(DataCy.selectionModal);
      }

      cy.logout();
    });
  });

  describe("Project List", () => {
    describe("I can reload my list of projects", () => {
      it("Shows the list of projects", () => {
        cy.getCy(DataCy.selectionModal).within(() => {
          cy.withinTableRows(DataCy.selectionProjectList, (tr) =>
            tr.should("have.length.above", 1)
          );
        });
      });

      it("Reloads the list of projects", () => {
        cy.getCy(DataCy.selectionModal).within(() => {
          cy.clickButton(DataCy.selectionReload, "first");

          cy.withinTableRows(DataCy.selectionProjectList, (tr) =>
            tr.should("have.length.above", 1)
          );
        });
      });
    });

    describe("I can search for projects by name", () => {
      it("Filters for projects that match my search", () => {
        cy.getCy(DataCy.selectionModal).within(() => {
          cy.inputText(DataCy.selectionSearch, testProject.name);

          cy.withinTableRows(DataCy.selectionProjectList, (tr) =>
            tr.should("contain.text", testProject.name)
          );
        });
      });

      it("Displays no projects when none match", () => {
        cy.getCy(DataCy.selectionModal).within(() => {
          cy.inputText(DataCy.selectionSearch, "$".repeat(20));

          cy.getCy(DataCy.selectionProjectList).within(() => {
            cy.get("tr").should("have.length", 2);
          });
        });
      });
    });

    describe("I can select a project to see its versions", () => {
      it("Selects a project and continues to the version step", () => {
        cy.getCy(DataCy.selectionModal).within(() => {
          cy.withinTableRows(DataCy.selectionProjectList, (tr) => {
            tr.get(".v-simple-checkbox").last().click();
          });

          cy.getCy(DataCy.stepperBackButton).should("not.be.disabled");
        });
      });

      it("Cannot continue without a project selected", () => {
        cy.getCy(DataCy.selectionModal).within(() => {
          cy.withinTableRows(DataCy.selectionProjectList, (tr) => {
            tr.get(".v-simple-checkbox").first().click();
          });

          cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
        });
      });
    });
  });

  describe("Project CRUD", () => {
    it("I can create an empty project", () => {
      cy.getCy(DataCy.selectionModal).within(() => {
        cy.clickButton(DataCy.selectorAddButton);
      });

      cy.getCy(DataCy.selectionEditModal).within(() =>
        cy.setProjectIdentifier("modal").clickButton(DataCy.selectionSaveButton)
      );

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });

    it("As an admin, I can edit a project's name and description", () => {
      cy.getCy(DataCy.selectionModal).within(() => {
        cy.clickButton(DataCy.selectorEditButton, "first");
      });

      cy.getCy(DataCy.selectionEditModal).within(() =>
        cy
          .getCy(DataCy.selectionNameInput)
          .type(" Edited")
          .clickButton(DataCy.selectionSaveButton)
      );

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });

    it("As an owner, I can delete a project", () => {
      cy.getCy(DataCy.selectionModal).within(() => {
        cy.clickButton(DataCy.selectorDeleteButton, "first");
      });

      cy.getCy(DataCy.selectionDeleteModal).within(() => {
        cy.getCy(DataCy.modalTitle)
          .invoke("text")
          .then((text) =>
            cy.inputText(
              DataCy.selectionDeleteNameInput,
              text.split(":")[1].trim()
            )
          );

        cy.clickButton(DataCy.selectionDeleteButton);
      });

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
    });
  });

  describe("Project Version List", () => {
    describe("I can reload my list of project versions", () => {
      it("Displays project versions", () => {
        cy.getCy(DataCy.selectionModal).within(() => {
          cy.clickButton(DataCy.stepperContinueButton);

          cy.withinTableRows(DataCy.selectionVersionList, (tr) =>
            tr.should("have.length.above", 1)
          );
        });
      });

      it("Reloads project versions", () => {
        cy.getCy(DataCy.selectionModal).within(() => {
          cy.clickButton(DataCy.stepperContinueButton);

          cy.clickButton(DataCy.selectionReload, "last");

          cy.withinTableRows(DataCy.selectionVersionList, (tr) =>
            tr.should("have.length.above", 1)
          );
        });
      });
    });

    describe("I can select and load a version of the project", () => {
      it("Selects and loads a project and version", () => {
        cy.getCy(DataCy.selectionModal).within(() => {
          cy.clickButton(DataCy.stepperContinueButton).clickButton(
            DataCy.stepperContinueButton
          );
        });

        cy.getCy(DataCy.appLoading).should("be.visible");
      });

      it("Cannot continue if a version is not selected", () => {
        cy.getCy(DataCy.selectionModal).within(() => {
          cy.clickButton(DataCy.stepperContinueButton);

          cy.withinTableRows(DataCy.selectionVersionList, (tr) => {
            tr.get(".v-simple-checkbox").first().click();
          });

          cy.getCy(DataCy.stepperContinueButton).should("be.disabled");
        });
      });
    });
  });

  // describe("Project Version CRUD", () => {
  //   describe("I can create a new major, minor, or revision version", () => {
  //     it("Can create a new major version", () => {
  //       cy.getCy(DataCy.selectionModal).within(() => {
  //         cy.clickButton(DataCy.stepperContinueButton);
  //       });
  //     });
  //
  //     it("Can create a new minor version", () => {
  //       cy.getCy(DataCy.selectionModal).within(() => {
  //         cy.clickButton(DataCy.stepperContinueButton);
  //       });
  //     });
  //
  //     it("Can create a new revision version", () => {
  //       cy.getCy(DataCy.selectionModal).within(() => {
  //         cy.clickButton(DataCy.stepperContinueButton);
  //       });
  //     });
  //   });
  //
  //   describe("I can upload new flat files to a project version");
  //
  //   describe("[WIP] I can upload flat files to the current document");
  //
  //   describe("I can delete a project version");
  // });
});
