/**
 * Represents all data cy selectors used in the app.
 */
export enum DataCy {
  // General

  stepperContinueButton = "generic-stepper-continue",

  // Authentication

  accountDropdown = "account-dropdown",
  emailInput = "input-email",
  passwordInput = "input-password",
  loginButton = "button-login",

  // Project Creation

  creationUploadButton = "button-create-project",

  creationBulkNameInput = "input-project-name-bulk",
  creationBulkDescriptionInput = "input-project-description-bulk",
  creationBulkFilesInput = "input-files-bulk",

  creationStandardNameInput = "input-project-name-standard",
  creationStandardDescriptionInput = "input-project-description-standard",
  creationStandardFilesInput = "input-files-panel",
  creationCreatePanelButton = "button-create-panel",
  creationTypeInput = "input-artifact-type",
  creationTypeButton = "button-artifact-type",
  creationArtifactButton = "button-artifact-dropbox",
  creationArtifactDeleteButton = "button-delete-artifact",
  creationEntitiesButton = "button-file-entities",
  creationIgnoreErrorsButton = "button-ignore-errors",

  // Jobs

  jobStatus = "job-status",
  jobPanel = "job-panel",
  jobDeleteButton = "button-delete-job",

  // Project Selection

  selectionModal = "modal-project-select",
  selectionProjectList = "table-project",
  selectionSearch = "input-selector-search",
  selectionReload = "button-selector-reload",
  selectionClose = "button-close",

  // Project settings
  settingsShareProject = "button-share-project",
}
