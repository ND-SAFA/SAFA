import "./baseCommands";
import "./dbCommands";
import "./shouldCommands";
import "./authenticationCommands";
import "./projectCreatorCommands";
import "./projectSelectionCommands";
import "./artifactCommands";
import "./traceLinkCommands";
import "./artifactTreeCommands";
import "./artifactTableCommands";
import "./timTreeCommands";
import "./projectDocumentCommands";
import "./projectSettingCommands";
import "./traceLinkGenerationCommands";
import "./customAttributesCommands";

/**
 * Ignore the following error:
 * - ResizeObserver loop limit exceeded
 * - Cannot read properties of _
 */
Cypress.on("uncaught:exception", (err) => {
  if (
    err.message.includes("ResizeObserver loop") ||
    err.message.includes("Cannot read properties of") ||
    err.message.includes("Cannot destructure property") ||
    err.message.includes("Session has timed out") ||
    err.message.includes("Unexpected end of JSON")
  ) {
    // ignore the error
    return false;
  }
});

/**
 * Generate users before running tests.
 */
before(() => {
  cy.log("Generating users...");
  cy.dbGenerateUsers();
  cy.expandViewport("l");
});

/**
 * Delete users after running tests.
 */
after(() => {
  cy.log("Cleaning up users...");
  cy.dbDeleteGeneratedUsers();
});
