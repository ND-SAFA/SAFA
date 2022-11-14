Cypress.Commands.add("openApproveGeneratedTraceLinks", () => {
  cy.clickButtonWithName("Trace Approval").switchTab("Trace Approval");
});
