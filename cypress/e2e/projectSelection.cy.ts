import { DataCy, testProject, validUser } from "../fixtures";

describe("Project Selection", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080")
      .login(validUser.email, validUser.password)
      .openProjectSelector()
      // Wait for projects to load.
      .wait(1000);
  });

  afterEach(() => {
    cy.closeModal(DataCy.selectionModal);
    cy.logout();
  });

  describe("Project List", () => {
    describe("I can reload my list of projects", () => {
      it("Shows the list of projects", () => {
        cy.getCy(DataCy.selectionModal).within(() => {
          cy.withinTableRows(DataCy.selectionProjectList, (tr) =>
            tr.should("have.length.above", 0)
          );
        });
      });

      it("Reloads the list of projects", () => {
        cy.getCy(DataCy.selectionModal).within(() => {
          cy.clickButton(DataCy.selectionReload).wait(1000);

          cy.withinTableRows(DataCy.selectionProjectList, (tr) =>
            tr.should("have.length.above", 0)
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

      it.only("Displays no projects when none match", () => {
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
            tr.first();
          });
        });
      });
    });
  });

  describe("Project CRUD", () => {});

  describe("Project Version List", () => {});

  describe("Project Version CRUD", () => {});
});
