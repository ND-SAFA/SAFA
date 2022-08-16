describe("Canvas", () => {
  beforeEach(() => {
    cy.visit(
      "http://localhost:8080/project?version=13801fc6-2483-4be4-920e-322edb9d8722"
    );
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
