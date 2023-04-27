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

before(() => {
  // Load users into the environment
  cy.loadEnv();

  // Now let's create these accounts
  cy.generateUsers();
});

/**
 * Ignore the following error:
 * - ResizeObserver loop limit exceeded
 * - Cannot read properties of _
 */

Cypress.on("uncaught:exception", (err) => {
  if (
    err.message.includes("ResizeObserver loop limit exceeded") ||
    err.message.includes("Cannot read properties of")
  ) {
    // ignore the error
    return false;
  }
});

after(() => {
  // Delete the users we created
  cy.deleteGeneratedUsers();

  // Clear the env
  cy.clearEnv();
});
