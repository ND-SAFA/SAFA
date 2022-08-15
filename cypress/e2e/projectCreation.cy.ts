import {
  validUser,
  simpleProjectFiles,
  simpleProjectFilesMap,
} from "../fixtures";

describe("Project Creation", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080/create").login(
      validUser.email,
      validUser.password
    );
  });

  describe("I can create a project from files uploaded in bulk", () => {
    beforeEach(() => {
      cy.switchTab("Bulk Upload");
    });

    it("cant create a project without a name", () => {
      cy.getCy("input-project-description", "last").type("A project");
      cy.uploadFiles("input-files", simpleProjectFilesMap.tim);

      cy.getCy("button-create-project").should("be.disabled");
    });

    it("cant create a project without any files", () => {
      cy.getCy("input-project-name", "last").type("Test Project");
      cy.getCy("input-project-description", "last").type("A project");

      cy.getCy("button-create-project").should("be.disabled");
    });

    it("can create a valid project", () => {
      cy.getCy("input-project-name", "last").type("Test Project");
      cy.getCy("input-project-description", "last").type("A project");
      cy.uploadFiles("input-files", ...simpleProjectFiles);

      cy.getCy("button-create-project").should("not.be.disabled").click();

      cy.getCy("job-status", "first", 5000)
        .wait(5000)
        .should("contain.text", "Completed");

      cy.clickButton("job-panel").clickButton("button-delete-job");
    });
  });
});
