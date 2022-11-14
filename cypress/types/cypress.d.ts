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

    chainRequest<T>(
      cb: (data: Subject) => Partial<RequestOptions>
    ): Chainable<Response<T>>;

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

    /**
     * Removes all stored documents on the most recent project.
     */
    dbResetDocuments(): Chainable<void>;

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

    /**
     * Logs into the create project page, uploads a project, and waits for it to complete.
     */
    loadNewProject(): Chainable<void>;

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
     * Fills inputs in the artifact modal.
     * The artifact name, type, and body will be filled with preset values if not set.
     *
     * @param props - The artifact fields to set.
     */
    fillArtifactModal(props: ArtifactFields): Chainable<void>;

    /**
     * Creates a new artifact from the artifact fab button.
     * Does not click the save button on the artifact, leaving the modal open.
     *
     * @param props - The artifact fields to set.
     */
    createNewArtifact(props: ArtifactFields): Chainable<void>;

    /**
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
     * Does not click the save button on the trace link, leaving the modal open.
     *
     * @param sourceName - The name of the source artifact.
     * @param targetName - The name of the target artifact.
     */
    createNewTraceLink(
      sourceName?: string,
      targetName?: string
    ): Chainable<void>;

    /**
     * Creates a new account on start page.
     * Should ideally be used before running a test that requires a new account.
     *
     * @param email - The email to create the account with.
     * @param password - The password to create the account with.
     */
    createNewAccount(email: string, password: string): Chainable<void>;

    /**
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
     * Waits for a project to load.
     *
     * @param waitForNodes - If true, this will wait for nodes to be painted on the graph.
     */
    waitForProjectLoad(waitForNodes?: boolean): Chainable<void>;

    /**
     * Logs in to the project page and waits for the most recent project to load.
     *
     * @param waitForNodes - If true, this will wait for nodes to be painted on the graph.
     */
    loadCurrentProject(waitForNodes?: boolean): Chainable<void>;

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

    /**
     * Adds a new artifact to the table view.
     *
     * @param name - The name of the artifact to add.
     * @param type - The type of the artifact to add.
     * @param docType - The document type of the artifact to add.
     * @param parentArtifact - The parent type of the artifact to add.
     * @param body - The body of the artifact to add.
     * @param summary - The summary of the artifact to add.
     */
    addTableArtifact(
      name: string,
      type: string,
      docType: string,
      parentArtifact: string,
      body: string,
      summary: string
    ): Chainable<void>;

    /**
     * Centers the graph.
     */
    centerGraph(): Chainable<void>;

    /**
     * Selects an artifact on the graph.
     * @param name - The artifact name to select.
     */
    selectArtifact(name: string): Chainable<void>;

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
     * Does not save the document, leaving the modal open.
     *
     * @param props - The document fields to set.
     *                The name will be added if not set.
     */
    createDocument(props: DocumentFields): Chainable<void>;

    /**
     * Saves the current document
     * The document modal must be open.
     */
    saveDocument(): Chainable<void>;

    /**
     * Uploads file containing trace links.
     * @param file - Contains trace links.
     */
    uploadingTraceLinks(file: string): Chainable<void>;

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

    /**
     * Navigates to the Approve Generated Trace Links page.
     *
     */
    openApproveGeneratedTraceLinks(): Chainable<void>;
    /**
     * Loads in a new project with generated trace links.
     *
     */
    loadNewGeneratedProject(): Chainable<void>;
  }
}
