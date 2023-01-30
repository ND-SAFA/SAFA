import { before } from "mocha";
import { DataCy } from "../../fixtures";
import { validUser } from "../../fixtures/data/user.json";

describe("Custom Attributes", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().clearCookies();

    cy.visit("/login")
      .login(validUser.email, validUser.password)
      .location("pathname", { timeout: 2000 });

    cy.visit("/create");

    cy.createBulkProject()
      .waitForJobLoad()
      .clickButton(DataCy.jobOpenButton)
      .openApproveGeneratedTraceLinks()
      .clickButton(DataCy.sidebarCloseButton);
  });

  describe("Custom Attributes CRUD", () => {
    const customAttribute = {
      Key: "Test Key",
      Label: "Test Label",
      Min: "0",
      Max: "1000",
    };

    beforeEach(() => {
      cy.viewport(1024, 768);
      cy.dbResetVersions();

      cy.visit("/login")
        .login(validUser.email, validUser.password)
        .location("pathname", { timeout: 2000 })
        .should("equal", "/");

      cy.getCy(DataCy.navOpenProjectButton).click();
      cy.withinTableRows(DataCy.selectionProjectList, (tr) => {
        tr.should("have.length", 2);
        tr.last().click();
      });

      cy.withinTableRows(DataCy.selectionVersionList, (tr) => {
        tr.should("have.length", 3).should("all.be.visible");
        tr.get("tbody").contains("2").click();
      });

      cy.getCy(DataCy.artifactTree).should("be.visible");
    });

    describe("I can add a custom attribute to my project", () => {
      // TODO: Add a custom attribute to the project
      it("Adds a custom attribute to the project", () => {
        cy.clickButton(DataCy.navSettingsButton);
        cy.clickButtonWithName("Custom Attributes");
        cy.clickButton(DataCy.addAttributeButton);

        // Fill in the form for the attribute
        cy.getCy(DataCy.attributeKeyInput).type(customAttribute.Key);
        cy.getCy(DataCy.attributeLabelInput).type(customAttribute.Label);

        // This selector is disabled in the css from any key or mouse input
        // cy.getCy(DataCy.attributeTypeInput).click().type("{downArrow}{enter}");

        cy.getCy(DataCy.attributeMinInput).type(customAttribute.Min);
        cy.getCy(DataCy.attributeMaxInput).type(customAttribute.Max);
        cy.clickButton(DataCy.attributeSaveButton);

        // Verify that the attribute was added
        cy.getCy(DataCy.snackbarSuccess).should("be.visible");
        cy.getCy(DataCy.attributeTableItem).should("be.visible");
      });
    });

    describe("I can edit a custom attribute on my project", () => {
      it("Creates a custom attribute and edits it", () => {
        cy.clickButton(DataCy.navSettingsButton);
        cy.clickButtonWithName("Custom Attributes");
      });
    });

    describe("I can delete a custom attribute on my project", () => {});

    describe.skip("I can generate FMEA attributes for traced artifact children", () => {
      // TODO: Add this test once FMEA attributes are implemented
    });

    describe.skip("I cannot change the key or data type of a custom attribute", () => {
      // TODO: Add this test one this feature is stable to implement
    });
  });
});
