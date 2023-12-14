import { DataCy } from "@/fixtures";

const inviteUser = Cypress.env("inviteUser");

describe("Project Members Display", () => {
  before(() => {
    cy.initEmptyProject()
      .initProjectVersion(false)
      .openProjectSettings()
      .switchTab("Members");

    cy.projectAddNewMember(inviteUser.email, "Admin");
  });

  beforeEach(() => {
    cy.initProjectVersion(false);
    cy.getCy(DataCy.appLoading).should("not.exist");
    cy.openProjectSettings().switchTab("Members");
  });

  describe("I can search through a project’s members", () => {
    it("Can search for a specific member", () => {
      cy.getCy(DataCy.selectorSearchInput).first().type(inviteUser.email);

      cy.withinTableRows(DataCy.projectSettingsTable, (tr) => {
        tr.contains(inviteUser.email).should("have.length", 1);
      });
    });
  });

  describe("I can see a project’s members", () => {
    it("Can display all project members", () => {
      cy.withinTableRows(DataCy.projectSettingsTable, (tr) => {
        // 1 header, 2 members.
        tr.should("have.length", 1 + 2);
      });
    });
  });
});
