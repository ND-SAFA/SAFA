/* eslint-disable max-lines */

/**
 * The position of an element within a list.
 */
type ElementPosition = "first" | "last";

/**
 * Represents the fields that can be filled in to create an artifact.
 */
interface ArtifactFields {
  name?: string;
  type?: string;
  body?: string;
  parent?: string;
}

/**
 * Represents the fields that can be filled in to create a document.
 */
interface DocumentFields {
  name?: string;
  type?: string;
  includeTypes?: string;
  artifacts?: string;
  includeChildTypes?: string;
  childArtifacts?: string;
}

declare namespace Cypress {
  interface Chainable<Subject> {
    // Database Cleanup

    /**
     * Chains together requests that return data.
     * @param cb - The request options that return data.
     * @return Chainable with request data.
     */
    chainRequest<T>(
      cb: (data: Subject) => Partial<RequestOptions>
    ): Chainable<Response<T>>;

    /**
     * Gets an api token.
     */
    dbToken(): Chainable<void>;

    /**
     * Removes all stored jobs.
     */
    dbResetJobs(): Chainable<void>;

    /**
     * Removes all stored projects.
     */
    dbResetProjects(): Chainable<void>;

    /**
     * Deletes all additional project versions, and creates a new version.
     */
    dbResetVersions(): Chainable<void>;

    /**
     * Removes all stored documents on the most recent project.
     */
    dbResetDocuments(): Chainable<void>;

    /**
     * Removes specified user from database.
     *
     * @param email - The user's email.
     * @param password - The user's password.
     */
    dbDeleteUser(email: string, password: string): Chainable<void>;

    // Should Commands

    /**
     * Asserts that the current location matches the given route.
     *
     * @param route - Thee route that should match the location.
     */
    locationShouldEqual(route: string): Chainable<void>;

    // Base Commands

    /**
     * Expands the viewport to a preset size.
     */
    expandViewport(size?: "m" | "l"): Chainable<void>;

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
     * @param force - If true, the click is forced.
     */
    clickButton(
      dataCy: string,
      elementPosition?: ElementPosition,
      force?: boolean
    ): Chainable<void>;

    /**
     * Finds last button with given name within it and clicks it.
     * @param name - Name of button.
     */
    clickButtonWithName(name: string): Chainable<void>;

    /**
     * Clicks option with given name in first select menu found.
     * @param dataCy - The select input to open.
     * @param optionName - Name of option to click.
     */
    clickSelectOption(dataCy: string, optionName: string): Chainable<void>;

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
     * @param waitForLoad - Defaults to true. Waits for the table to stop loading.
     */
    withinTableRows(
      dataCy: string,
      fn: (tr: Chainable<JQuery<HTMLElement>>) => void,
      waitForLoad?: boolean
    ): Chainable<void>;

    // Authentication Commands

    /**
     * Creates a new account on start page.
     * Should ideally be used before running a test that requires a new account.
     *
     * @param email - The email to create the account with.
     * @param password - The password to create the account with.
     */
    createNewAccount(email: string, password: string): Chainable<void>;

    /**
     * Logs into the app with the given credentials.
     *
     * @param email - The email to log in with.
     * @param password - The password to log in with.
     */
    login(email: string, password: string): Chainable<void>;

    /**
     * Logs into a specific page with the given credentials.
     *
     * @param email - The email to log in with.
     * @param password - The password to log in with.
     * @param route - The route to navigate to.
     * @param query - Any query parameters to include.
     */
    loginToPage(
      email: string,
      password: string,
      route: string,
      query?: Record<string, string>
    ): Chainable<void>;

    /**
     * Logs out of the app.
     */
    logout(): Chainable<void>;

    // Project Creation

    /**
     * Clears the DB of existing projects and jobs.
     * Logs into the create project page and creates an empty project.
     * The user will remain logged in on the artifact view page.
     */
    initEmptyProject(): Chainable<void>;

    /**
     * Clears the DB of existing projects and jobs.
     * Logs into the create project page and creates a bulk project.
     * The user will remain logged in on the job status page.
     *
     * @param waitForComplete - Defaults to true. Whether to wait for the creation job to complete.
     */
    initProject(waitForComplete?: boolean): Chainable<void>;

    /**
     * Clears the DB of existing project versions.
     * Logs into the open project page and creates a new project version.
     * The user will remain logged in on the artifact view page.
     *
     * @param waitForComplete - Defaults to true. Whether to wait for the artifact tree to display nodes.
     */
    initProjectVersion(waitForComplete?: boolean): Chainable<void>;

    /**
     * @deprecated
     * Creates a new bulk upload project.
     */
    createBulkProject(): Chainable<void>;

    /**
     * @deprecated
     * Logs into the create project page, uploads a project, and waits for it to complete.
     * The user will be logged out.
     */
    loadNewProject(): Chainable<void>;

    /**
     * Setting the project name and description within the project creator.
     *
     * @param type - The type of project identifier to set.
     */
    setProjectIdentifier(type: "bulk" | "standard" | "modal"): Chainable<void>;

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
     * Navigates to the settings page and upload flat files tab.
     */
    openUploadFiles(): Chainable<void>;

    /**
     * Waits for the most recent job to complete.
     */
    waitForJobLoad(): Chainable<void>;

    // Project Selection

    /**
     * Opens the project selector page.
     */
    openProjectSelector(): Chainable<void>;

    /**
     * Must have the project selector open.
     * On the project step: Selects the current project, continuing to the version step.
     * On the version step: Selects the current version, continuing to the project page.
     *
     * @param select - If set, the first project or version will be selected before continuing.
     */
    projectSelectorContinue(select?: "project" | "version"): Chainable<void>;

    /**
     * Must have the project selector open to the version step.
     * Creates a new version of the given type.
     */
    createNewVersion(type: "major" | "minor" | "revision"): Chainable<void>;

    // Artifact View

    /**
     * Fills inputs in the artifact modal.
     * The artifact name, type, and body will be filled with preset values if not set.
     *
     * @param props - The artifact fields to set.
     */
    fillArtifactModal(props: ArtifactFields): Chainable<void>;

    /**
     * Creates a new artifact from the artifact fab button.
     *
     * @param props - The artifact fields to set.
     * @param save - Defaults to false. Whether to save the artifact or keep the panel open.
     */
    createNewArtifact(props: ArtifactFields, save?: boolean): Chainable<void>;

    /**
     * @deprecated
     * Saves the artifact that is currently open in the creator modal.
     */
    saveArtifact(): Chainable<void>;

    /**
     * Fills in inputs within the trace link modal.
     *
     * @param sourceName - The name of the source artifact.
     * @param targetName - The name of the target artifact.
     */
    fillTraceLinkModal(
      sourceName?: string,
      targetName?: string
    ): Chainable<void>;

    /**
     * Creates a new trace link from the artifact fab button.
     *
     * @param sourceName - The name of the source artifact.
     * @param targetName - The name of the target artifact.
     * @param save - Defaults to false. Whether to save the trace link or keep the panel open.
     */
    createNewTraceLink(
      sourceName?: string,
      targetName?: string,
      save?: boolean
    ): Chainable<void>;

    /**
     * @deprecated
     * Saves the trace link that is currently open in the creator modal.
     */
    saveTraceLink(): Chainable<void>;

    // Artifact Tree

    /**
     * Get a node on the graph by name
     *
     * @param name - The name of the node to find.
     */
    getNode(name: string): Chainable<JQuery<HTMLElement>>;

    /**
     * Gets nodes on the graph.
     *
     * @param selected - If true, only the selected node is returned.
     */
    getNodes(selected?: boolean): Chainable<JQuery<HTMLElement>>;

    /**
     * Waits for the artifact tree to load.
     *
     * @param waitForNodes - If true, this will wait for nodes to be painted on the graph.
     */
    waitForProjectLoad(waitForNodes?: boolean): Chainable<void>;

    /**
     * @deprecated
     * Logs in to the project page and waits for the most recent project to load.
     *
     * @param waitForNodes - If true, this will wait for nodes to be painted on the graph.
     */
    loadCurrentProject(waitForNodes?: boolean): Chainable<void>;

    /**
     * Centers the graph.
     */
    centerGraph(): Chainable<void>;

    /**
     * Selects an artifact on the graph.
     *
     * @param name - The artifact name to select.
     */
    selectArtifact(name: string): Chainable<void>;

    // Artifact Table

    /**
     * Switches to table view.
     */
    switchToTableView(): Chainable<void>;

    /**
     * Looks up the first element in the artifact table view by node name.
     */
    artifactTableFirstElementLookUp(): Chainable<void>;

    /**
     * Sorts the artifact table by the given sort type.
     *
     * @param sortType - The type of sort to use.
     */
    artifactTableChangeSort(sortType: string): Chainable<void>;

    // Project Documents

    /**
     * Opens the document selector.
     */
    openDocumentSelector(): Chainable<void>;

    /**
     * Opens the document creator.
     */
    openDocumentCreator(): Chainable<void>;

    /**
     * Opens the document editor for the document with the given name.
     *
     * @param name - TRhe document to open.
     */
    openDocumentEditor(name: string): Chainable<void>;

    /**
     * Fills the document modal fields.
     * The document modal must be open.
     *
     * @param props - The document fields to set.
     *                The name will be added if not set.
     */
    fillDocumentFields(props: DocumentFields): Chainable<void>;

    /**
     * Creates a new document.
     *
     * @param props - The document fields to set.
     *                The name will be added if not set.
     * @param save. Defaults to false. Whether to save the document or leave the panel open.
     */
    createDocument(props: DocumentFields, save?: boolean): Chainable<void>;

    /**
     * @deprecated
     * Saves the current document
     * The document modal must be open.
     */
    saveDocument(): Chainable<void>;

    // Project Settings

    /**
     * Opens the project settings modal.
     */
    openProjectSettings(): Chainable<void>;

    /**
     * Adds New member into a project
     * Must be in project settings.
     * @param name - Input email of new member.
     * @param projectRole - Input project role such as "owner", "Editor", "Viewer", "Admin"
     */
    projectAddNewMember(name: string, projectRole: string): Chainable<void>;

    // Trace Approval

    /**
     * Navigates to the Approve Generated Trace Links page.
     */
    openApproveGeneratedTraceLinks(): Chainable<void>;
  }
}
