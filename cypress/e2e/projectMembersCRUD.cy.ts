import { DataCy, validUser } from "../fixtures";

describe("Project Members CRUD", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080/settings").login(
      validUser.email,
      validUser.password
    );

    cy.openProjectSelector();

    cy.clickButton(DataCy.stepperContinueButton);
    cy.clickButtonWithName("submit");
    cy.wait(100);

    cy.projectSettingsSelector();
  });
  describe("As an owner, I can add a new member to a project", () => {
    it.only("Cant add an invalid member", () => {
      cy.clickButton(DataCy.settingsShareProject);
      cy.clickButtonWithName("User Email").type("Alex Rodriguez");
    });
    it("Adds a new member to a project", () => {});
  });
  describe.skip("As an owner, I can edit a project members permissions", () => {
    it("Edits the permissions of a project member", () => {});
  });
  describe.skip("As an owner, I can remove a member from a project", () => {
    it("Removes a project member", () => {});
  });
});
