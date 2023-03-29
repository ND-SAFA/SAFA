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

/* Ignore the following error:
 * ResizeObserver loop limit exceeded
 */
Cypress.on("uncaught:exception", (err) => {
  if (err.message.includes("ResizeObserver loop limit exceeded")) {
    // ignore the error
    return false;
  }
});
