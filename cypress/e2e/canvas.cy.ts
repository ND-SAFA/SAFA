describe("Canvas", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8080/project");
  });

  it("can interact with the canvas", () => {
    const validTestUser = {
      email: "tjnewman111@gmail.com",
      password: "123",
    };

    cy.login(validTestUser.email, validTestUser.password);

    // Validates that artifacts appear on the graph.
    cy.get(".artifact-container").should("be.visible");

    // Opens the right click window.
    cy.get("canvas")
      .first()
      .then(($el) =>
        cy.wrap($el).rightclick($el.width() / 2, $el.height() / 2)
      );

    // Click the add artifact button.
    cy.get("#add-artifact")
      .should("be.visible")
      .then(($el) => $el.click());

    // Validates that the add artifact window is open.
    cy.contains("label", "Create Artifact").should("be.visible");
  });
});
