import { user } from "@/fixtures/data/user";
export const beforeAllTests = () => {
  /**
   * Run the following command before any test suits
   * - This will create a new user and login for that user
   */
  before(() => {
    // First generate all the users that are needed for the test suit
    cy.generateUsers();
    console.log("Valid user: ", user.validUser);
  });

  /**
   * Delete all the users that were created for the test suit
   */
  after(() => {
    cy.deleteGeneratedUsers();
  });
};
