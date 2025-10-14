import { DataCy, Routes, testProject } from "@/fixtures";

describe("Projects", () => {
  beforeEach(() => {
    cy.initEmptyProject();

    cy.expandViewport()
      .visit(Routes.MY_PROJECTS)
      .locationShouldEqual(Routes.MY_PROJECTS);
  });

  describe("As an admin, I can edit a project's name and description", () => {
    const editedName = " - Edited";

    it("Edits a project from the selector", () => {
      cy.clickButton(DataCy.selectorEditButton, "first");

      cy.getCy(DataCy.projectEditModal).within(() =>
        cy
          .getCy(DataCy.projectEditNameInput)
          .type(editedName)
          .clickButton(DataCy.projectEditSaveButton)
      );

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.contains(editedName).should("be.visible");
    });

    it("Edits a project from the settings", () => {
      cy.projectSelectorContinue("project").projectSelectorContinue("version");

      cy.getCy(DataCy.appLoading).should("not.exist");

      cy.clickButton(DataCy.navSettingsButton).clickButton(
        DataCy.projectSettingsEditButton
      );

      cy.getCy(DataCy.projectEditNameInput)
        .type(editedName)
        .clickButton(DataCy.projectEditSaveButton);

      cy.getCy(DataCy.snackbarSuccess).should("be.visible");
      cy.contains(editedName).should("be.visible");
    });
  });

  describe.skip("As an owner, I can delete a project", () => {
    it("Deletes a project from the selector", () => {
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

    it("Deletes a project from the settings", () => {
      cy.projectSelectorContinue("project").projectSelectorContinue("version");

      cy.getCy(DataCy.appLoading).should("not.exist");

      cy.clickButton(DataCy.navSettingsButton).clickButton(
        DataCy.projectSettingsDeleteButton
      );

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
