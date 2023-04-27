import { DataCy } from "@/fixtures";
const user = Cypress.env();

describe("Project Members Display", () => {
  before(() => {
    cy.initEmptyProject();
    cy.getCy(DataCy.appLoading).should("not.exist");
    cy.openProjectSettings();

    cy.projectAddNewMember(user.inviteUser.email, "Admin");
  });

  beforeEach(() => {
    cy.initProjectVersion(false);
    cy.getCy(DataCy.appLoading).should("not.exist");
    cy.openProjectSettings();
  });

  describe("I can search through a project’s members", () => {
    it("Can search for a specific member", () => {
      cy.getCy(DataCy.selectorSearchInput).first().type(user.inviteUser.email);

      cy.withinTableRows(DataCy.projectSettingsTable, (tr) => {
        tr.contains(user.inviteUser.email).should("have.length", 1);
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
