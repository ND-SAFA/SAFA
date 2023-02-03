import { DataCy } from "@/fixtures";
import { inviteUser } from "@/fixtures/data/user.json";

describe("Project Members Display", () => {
  before(() => {
    cy.initEmptyProject().openProjectSettings();

    cy.projectAddNewMember(inviteUser.email, "Admin");
  });

  beforeEach(() => {
    cy.initProjectVersion(false).openProjectSettings();
  });

  describe("I can search through a project’s members", () => {
    it("Can search for a specific member", () => {
      cy.getCy(DataCy.projectSettingsSearchUser).first().type(inviteUser.email);

      cy.withinTableRows(DataCy.projectSettingsTable, (tr) => {
        tr.contains(inviteUser.email).should("have.length", 1);
      });
    });
  });

  describe("I can see a project’s members", () => {
    it("Can display all project members", () => {
      cy.withinTableRows(DataCy.projectSettingsTable, (tr) => {
        // There should be 3 (Heading, owner, and added user).
        tr.should("have.length", 3);
      });
    });
  });
});
