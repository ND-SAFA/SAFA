/**
 * The position of an element within a list.
 */
type ElementPosition = "first" | "last";

declare namespace Cypress {
  interface Chainable<Subject> {
    // Database Cleanup

    /**
     * Gets an api token.
     */
    dbToken(): Chainable<Cypress.Response<{ token: string }>>;

    /**
     * Removes all stored jobs.
     */
    dbResetJobs(): Chainable<void>;

    /**
     * Removes all stored projects.
     */
    dbResetProjects(): Chainable<void>;

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
     * Returns whether an element exists.
     * Should not be used in tests, only in before-each cleanup calls.
     *
     * @param dataCy - The testing selector to find.
     * @return Whether the element exists.
     */
    doesExist(dataCy: string): Chainable<boolean>;

    /**
     * Sets the value of an input field.
     *
     * @param dataCy - The testing selector of the input being set.
     * @param inputValue - The value to set.
     * @param clear - If true, the input will be cleared first.
     */
    inputText(
      dataCy: string,
      inputValue: string,
      clear?: boolean
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

    /**
     * Runs a callback on all rows of a table.
     *
     * @param dataCy - The testing selector of the table.
     * @param fn - A callback run on each row of the table.
     */
    withinTableRows(
      dataCy: string,
      fn: (tr: Chainable<JQuery<HTMLElement>>) => void
    ): Chainable<void>;

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
    setProjectIdentifier(type: "bulk" | "standard" | "modal"): Chainable<void>;

    /**
     * Creates a new bulk upload project.
     */
    createBulkProject(): Chainable<void>;

    /**
     * Opens the last file panel after waiting for it to close when files are parsed.
     */
    openPanelAfterClose(): Chainable<void>;

    /**
     * Creates artifacts - inputs description and uploads file.
     *
     * @param name - The name of the artifact typeto create.
     * @param file - The file that belongs to the artifact.
     * @param next - If true, proceeds to the next step.
     */
    createArtifactPanel(
      name: string,
      file: string,
      next?: boolean
    ): Chainable<void>;

    /**
     * Creates trace matrix - selects source or target then selects artifact.
     *
     * @param sourceType - The first type artifact you want to select in the source (ex. requirement).
     * @param targetType - The second type of artifact you want to select for target (ex. hazard).
     * @param file - The file that belongs to the trace link (ex. hazard2hazard).
     *               If none, is set, this will not be uploaded, and the stepper will not continue.
     * @param next - If true, proceeds to the next step.
     */
    createTraceMatrix(
      sourceType: string,
      targetType: string,
      file?: string,
      next?: boolean
    ): Chainable<void>;

    /**
     * Creates artifacts & a trace matrix for requirements and hazards.
     *
     * @param createTraces - If true, traces will be created between the artifact types.
     * @param next - If true, proceeds to the final step.
     */
    createReqToHazardFiles(
      createTraces?: boolean,
      next?: boolean
    ): Chainable<void>;

    /**
     * Opens the upload flat files modal.
     */
    openUploadFiles(): Chainable<void>;

    // Project Selection

    /**
     * Opens the project selection modal.
     */
    openProjectSelector(): Chainable<void>;

    /**
     * Must have the project selector open.
     * On the project step: Selects the current project, continuing to the version step.
     * On the version step: Selects the current version, continuing to the project page.
     */
    projectSelectorContinue(): Chainable<void>;

    /**
     * Must have the project selector open to the version step.
     * Creates a new version of the given type.
     */
    createNewVersion(type: "major" | "minor" | "revision"): Chainable<void>;

    // Artifact View

    /**
     * Creates a new artifact from the artifact fab button.
     * Does not click the save button on the artifact, leaving the modal open.
     *
     * @param name - A specific name to set.
     * @param type - A specific type to set.
     * @param body - A specific body to set.
     */
    createNewArtifact(
      name?: string,
      type?: string,
      body?: string
    ): Chainable<void>;
  }
}
