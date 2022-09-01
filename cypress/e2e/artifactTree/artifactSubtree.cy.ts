describe("Artifact Subtree", () => {
  before(() => {
    cy.dbResetJobs().dbResetProjects().loadNewProject();
  });

  beforeEach(() => {
    cy.loadCurrentProject();
  });

  describe("I can hide an artifact’s subtree", () => {
    it("Hides the subtree below an artifact", () => {
      // Assert that child nodes are not visible
    });
  });

  describe("I can show an artifact’s subtree", () => {
    it("Hides the subtree below an artifact", () => {
      // Assert that child nodes are made visible again
    });
  });

  describe("I can highlight an artifact’s subtree", () => {
    it("Hides the subtree below an artifact", () => {
      // Assert that old subtree is not faded
    });
  });

  describe("I can see how many children are hidden below a parent artifact", () => {
    it("Hides the subtree below an artifact", () => {
      // Assert that child node count equals hidden children
    });
  });
});
