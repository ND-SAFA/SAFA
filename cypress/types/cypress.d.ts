declare namespace Cypress {
  interface Chainable<Subject> {
    // Base Commands

    /**
     * Sets the value of an input field.
     *
     * @param inputLabel - The label of the input being set.
     * @param inputValue - The value to set.
     */
    inputText(inputLabel: string, inputValue: string): Chainable<void>;
    /**
     * Returns the button with the given label.
     *
     * @param buttonLabel - The label of the button to find.
     */
    getButton(buttonLabel: string): Chainable<JQuery<HTMLElement>>;
    /**
     * Clicks a button.
     *
     * @param buttonLabel - The label of the button to click.
     */
    clickButton(buttonLabel: string): Chainable<void>;

    // Authentication Commands

    /**
     * Logs into the app with the given credentials.
     *
     * @param email - The email to log in with.
     * @param password - The password to log in with.
     * @return Whether the login was successful.
     */
    login(email: string, password: string): Chainable<void>;
    /**
     * Logs out of the app.
     */
    logout(): Chainable<void>;
  }
}
