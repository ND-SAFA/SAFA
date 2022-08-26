/**
 * The position of an element within a list.
 */
type ElementPosition = "first" | "last";

declare namespace Cypress {
  interface Chainable<Subject> {
    // Base Commands

    /**
     * Gets an element based on the `data-cy` selector.
     *
     * @param dataCy - The testing selector to find.
     * @param elementPosition - Whether to return first or last element of query.
     * @param timeout - The timeout to optionally wait for.
     * @return The elements that match the given selector.
     */
    getCy(
      dataCy: string,
      elementPosition?: ElementPosition,
      timeout?: number
    ): Chainable<JQuery<HTMLElement>>;

    /**
     * Sets the value of an input field.
     *
     * @param dataCy - The testing selector of the input being set.
     * @param inputValue - The value to set.
     * @param elementPosition - The specific element to grab, if there are multiple.
     */
    inputText(
      dataCy: string,
      inputValue: string,
      elementPosition?: ElementPosition
    ): Chainable<void>;

    /**
     * Clicks a button.
     *
     * @param dataCy - The testing selector of the button to click.
     * @param elementPosition - The specific element to grab, if there are multiple.
     */
    clickButton(
      dataCy: string,
      elementPosition?: ElementPosition
    ): Chainable<void>;

    /**
     * Finds last button with given name within it and clicks it.
     * @param name - Name of button.
     */
    clickButtonWithName(name: string): Chainable<void>;

    /**
     * Clicks option with given name in first menu found.
     * @param optionName - Name of option to click.
     */
    clickMenuOption(optionName: string): Chainable<void>;

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

    /**
     * Closes a given modal.
     *
     * @param dataCy - The testing selector of the modal.
     */
    closeModal(dataCy: string): Chainable<void>;

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

    // Project Creation

    /**
     * Setting the project name and description within the project creator.
     *
     * @param type - The type of project identifier to set.
     */
    setProjectIdentifier(type: "bulk" | "standard"): Chainable<void>;

    // Project Selection

    /**
     * Opens the project selection modal.
     */
    openProjectSelector(): Chainable<void>;

    /**
     * Creates artifacts - inputs description and uploads file
     *
     * @param name - The name of the artifact you want
     * @param file - The file that belongs to the artifact
     */
    createArtifactPanel(name: string, string: string): Chainable<void>;

    /**
     * Creates trace matrix - selects source or target then selects artifact
     *
     * @param name - Name is the first type artifact you want to select in the source (ex. requirement)
     * @param artifact - Artifact is the second type of artifact you want to cselect for target (ex. hazard)
     */
    createTraceMatrix(name: string, artifact: string): Chainable<void>;

    /**
     * Uploads files to make Trace links
     *
     * @param file - The file that belongs to the trace link (ex. hazard2hazard)
     */
    uploadingTraceLinks(file: string): Chainable<void>;
  }
}
