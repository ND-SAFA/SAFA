describe.skip("Canvas", () => {
  beforeEach(() => {
    cy.visit("/project?version=daaa6838-a446-4b14-bb7a-dd343f855e06");
  });

  it("can interact with the canvas", () => {
    const user = {
      email: "tjnewman111@gmail.com",
      password: "123",
    };

    cy.login(user.email, user.password);

    // Validates that artifacts appear on the graph.
    cy.get(".artifact-svg-wrapper").should("be.visible");

    // Opens the right click window.
    cy.get("canvas")
      .first()
      .then(($el) => cy.wrap($el).rightclick(0, $el.height() / 2));

    // Click the add artifact button.
    cy.get("#add-artifact")
      .should("be.visible")
      .then(($el) => $el.click());

    // Validates that the add artifact window is open.
    cy.contains("span", "Create Artifact").should("be.visible");
  });
});
