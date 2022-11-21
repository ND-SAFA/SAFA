Cypress.Commands.add("openApproveGeneratedTraceLinks", () => {
  cy.clickButtonWithName("Trace Prediction").switchTab("Trace Approval");
});
