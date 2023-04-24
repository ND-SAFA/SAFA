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
import { user } from "fixtures/data/user";

/**
 * Ignore the following error:
 * - ResizeObserver loop limit exceeded
 * - Cannot read properties of _
 */
before(() => {
  // Export the user object so it stays constant
  // and can be used in the tests
  const userObject = user;

  // Generate the accounts that we need for the tests
});

Cypress.on("uncaught:exception", (err) => {
  if (
    err.message.includes("ResizeObserver loop limit exceeded") ||
    err.message.includes("Cannot read properties of")
  ) {
    // ignore the error
    return false;
  }
});
