import { DataCy, validUser } from "../fixtures";

describe("Project Selection", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080").login(
      validUser.email,
      validUser.password
    );
  });

  afterEach(() => {
    cy.logout();
  });

  describe("Project List", () => {
    describe("I can reload my list of projects", () => {
      it("Shows the list of projects", () => {
        cy.clickButtonWithName("Project").clickButtonWithName("Open Project");

        // Wait for projects to load.
        cy.wait(1000);

        cy.getCy(DataCy.selectionProjectList).within(() => {
          cy.get("tr").should("have.length.above", 0);
        });
        cy.getCy(DataCy.selectionModal).within(() =>
          cy.clickButton(DataCy.selectionClose)
        );
      });

      it("Reloads the list of projects", () => {});
    });

    describe("I can search for projects by name", () => {});

    describe("I can select a project to see its versions", () => {});
  });

  describe("Project CRUD", () => {});

  describe("Project Version List", () => {});

  describe("Project Version CRUD", () => {});
});
