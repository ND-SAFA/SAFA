declare namespace Cypress {
  interface Chainable<Subject> {
    // Base Commands

    /**
     * Gets an element based on the `data-cy` selector.
     *
     * @param dataCy - The testing selector to find.
     * @param timeout - The timeout to optionally wait for.
     * @return The elements that match the given selector.
     */
    getCy(dataCy: string, timeout?: number): Chainable<JQuery<HTMLElement>>;

    /**
     * Sets the value of an input field.
     *
     * @param dataCy - The testing selector of the input being set.
     * @param inputValue - The value to set.
     */
    inputText(dataCy: string, inputValue: string): Chainable<void>;

    /**
     * Clicks a button.
     *
     * @param dataCy - The testing selector of the button to click.
     */
    clickButton(dataCy: string): Chainable<void>;

    /**
     * Uploads files.
     *
     * @param dataCy - The testing selector of the file upload input.
     * @param filePaths - The paths to the files to upload.
     */
    uploadFiles(dataCy: string, ...filePaths: string[]): Chainable<void>;

    /**
     * Clicks to switch to a different tab.
     *
     * @param tabLabel - The label of the tab to click.
     */
    switchTab(tabLabel: string): Chainable<void>;

    // Authentication Commands

    /**
     * Logs into the app with the given credentials.
     *
     * @param email - The email to log in with.
     * @param password - The password to log in with.
     */
    login(email: string, password: string): Chainable<void>;

    /**
     * Logs out of the app.
     */
    logout(): Chainable<void>;

    // Project Creator Commands

    /**
     * Setting the project name and description within the standard project creator.
     * @param name - Project name.
     * @param description - Project description.
     */
    setProjectInformationInStandardUpload(
      name: string,
      description: string
    ): Chainable<void>;
  }
}
