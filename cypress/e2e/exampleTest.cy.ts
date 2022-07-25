import files from "../fixtures/simpleProjectFiles.json";
import { validUser } from "../fixtures/user.json";

describe("Project Creation", () => {
  // Epic
  beforeEach(() => {
    cy.visit("http://localhost:8080/create").login(
      validUser.email,
      validUser.password
    );
  });

  describe("Bulk Project Creation", () => {
    beforeEach(() => {
      cy.switchTab("Bulk Upload");
    });
    // Feature
    describe("I can create a project from flat files", () => {
      // User story
      it("can create a valid project", () => {
       
      }); // Individual tests for US
    });
  });
});
