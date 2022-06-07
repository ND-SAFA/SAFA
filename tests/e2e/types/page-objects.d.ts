import { EnhancedPageObject } from "nightwatch";

export type LoginPage = EnhancedPageObject<
  {
    /**
     * Sets the value of an input field.
     *
     * @param inputLabel - The label of the input being set.
     * @param inputValue - The value to set.
     */
    setInputText(inputLabel: string, inputValue: string): LoginPage;
    /**
     * Clicks a button.
     *
     * @param buttonLabel - The label of the button to click.
     */
    clickButton(buttonLabel: string): LoginPage;
    /**
     * Checks if a button can be clicked.
     *
     * @param buttonLabel - The label of the button to check.
     * @param testLabel - The label of the test checking whether the button is clickable.
     */
    isButtonClickable(buttonLabel: string, testLabel: string): LoginPage;
    /**
     * Logs in to a session.
     *
     * @param email - The email to use.
     * @param password - The password to use.
     */
    loginSession(email: string, password: string): LoginPage;
    /**
     * Checks that the login succeeded.
     */
    checkLoginSuccess(): LoginPage;
    /**
     * Checks that the login failed.
     */
    checkLoginFailure(): LoginPage;
  },
  {
    loginView: string;
    loginError: string;
    profileImage: string;
  }
>;
