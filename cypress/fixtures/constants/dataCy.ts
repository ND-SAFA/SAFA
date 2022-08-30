/**
 * Represents all data cy selectors used in the app.
 */
export enum DataCy {
  // General

  appLoading = "app-loading",

  // Navigation

  navProjectButton = "button-nav-project",
  navVersionButton = "button-nav-version",
  navLinksButton = "button-nav-links",
  navGraphCenterButton = "button-nav-graph=center",

  // Steppers

  stepperContinueButton = "button-stepper-continue",
  stepperBackButton = "button-stepper-back",

  // Selector Tables

  selectorAddButton = "button-selector-add",
  selectorEditButton = "button-selector-edit",
  selectorDeleteButton = "button-selector-delete",

  // Modals

  modalTitle = "modal-title",
  modalCloseButton = "button-close",
  confirmModalButton = "button-confirm-modal",

  // Authentication

  accountDropdown = "account-dropdown",
  emailInput = "input-email",
  passwordInput = "input-password",
  loginButton = "button-login",

  // Snackbar

  snackbarInfo = "snackbar-info",
  snackbarSuccess = "snackbar-success",
  snackbarWarning = "snackbar-warning",
  snackbarError = "snackbar-error",

  // Project Creation

  creationBulkNameInput = "input-project-name-bulk",
  creationBulkDescriptionInput = "input-project-description-bulk",
  creationBulkFilesInput = "input-files-bulk",

  creationStandardNameInput = "input-project-name-standard",
  creationStandardDescriptionInput = "input-project-description-standard",
  creationStandardFilesInput = "input-files-panel",
  creationCreatePanelButton = "button-create-panel",
  creationTypeInput = "input-artifact-type",
  creationTypeButton = "button-artifact-type",
  creationArtifactDeleteButton = "button-delete-artifact",
  creationEntitiesButton = "button-file-entities",
  creationIgnoreErrorsButton = "button-ignore-errors",
  creationDeletePanel = "button-delete-artifact",
  creationEntityButton = "button-created-entity",
  creationFilePanel = "panel-files",
  creationUploadButton = "button-create-project",

  // Jobs

  jobStatus = "job-status",
  jobPanel = "job-panel",
  jobDeleteButton = "button-delete-job",
  jobOpenButton = "button-open-job",

  // Project Selection

  selectionModal = "modal-project-select",
  selectionProjectList = "table-project",
  selectionVersionList = "table-version",
  selectionSearch = "input-selector-search",
  selectionReload = "button-selector-reload",

  projectEditModal = "modal-project-edit",
  projectEditNameInput = "input-project-name-modal",
  projectEditDescriptionInput = "input-project-description-modal",
  projectEditSaveButton = "button-project-save",

  projectDeleteModal = "modal-project-delete",
  projectDeleteNameInput = "input-project-delete-name",
  projectDeleteConfirmButton = "button-project-delete",

  versionCreateModal = "modal-version-create",
  versionCreateMajorButton = "button-create-major-version",
  versionCreateMinorButton = "button-create-minor-version",
  versionCreateRevisionButton = "button-create-revision-version",

  versionDeleteModal = "modal-version-delete",
  versionDeleteConfirmButton = "button-version-delete",

  versionUploadModal = "modal-version-upload",
  versionUploadFilesInput = "input-files-version",

  // Artifact View

  artifactFabToggle = "button-fab-toggle",
  artifactFabCreateArtifact = "button-fab-create-artifact",
  artifactFabCreateTrace = "button-fab-create-trace",
  artifactFabDrawTrace = "button-fab-draw-trace",

  artifactSaveModal = "modal-artifact-save",
  artifactSaveNameInput = "input-artifact-name",
  artifactSaveTypeInput = "input-artifact-type",
  artifactSaveBodyInput = "input-artifact-body",
  artifactSaveParentInput = "input-artifact-parent",
  artifactSaveSubmitButton = "button-artifact-save",

  traceSaveModal = "modal-trace-save",
  traceSaveSourceInput = "button-trace-save-source",
  traceSaveTargetInput = "button-trace-save-target",
  traceSaveSubmitButton = "button-trace-save",

  traceApproveModal = "modal-trace-approve",
  traceUnreviewButton = "button-trace-unreview",
  traceApproveButton = "button-trace-approve",
  traceDeclineButton = "button-trace-decline",
  traceDeleteButton = "button-trace-delete",

  // Selection Panel

  selectedPanelName = "text-selected-name",
  selectedPanelBodyButton = "button-selected-body",
  selectedPanelEditButton = "button-selected-edit",
  selectedPanelDeleteButton = "button-selected-delete",

  selectedPanelParents = "list-selected-parents",
  selectedPanelParentItem = "list-selected-parent-item",
  selectedPanelParentLinkButton = "button-selected-parent-link",
  selectedPanelChildren = "list-selected-children",
  selectedPanelChildItem = "list-selected-child-item",
  selectedPanelChildLinkButton = "button-selected-child-link",

  // Artifact Tree

  treeNode = "node-artifact-tree",
  treeSelectedNode = "node-artifact-tree-selected",
}

export enum DataIds {
  rightClickAddArtifact = "#add-artifact",
  rightClickDuplicateArtifact = "#duplicate-artifact",
}
