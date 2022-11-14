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
  navGraphCenterButton = "button-nav-graph-center",
  navToggleLeftPanel = "button-left-panel-toggle",
  navToggleRightPanel = "button-right-panel-toggle",
  navGraphFilterButton = "button-nav-graph-filter",
  navGraphFilterOption = "button-checkmark-menu-item",
  navToggleView = "button-view-toggle",

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

  // Account Creation

  newAccountEmailInput = "input-new-email",
  newAccountPasswordInput = "input-new-password",
  createAccountButton = "button-create-account",
  createAccountLoginButton = "button-create-account-login",

  // Authentication

  isLoggedIn = "is-logged-in",
  emailInput = "input-email",
  passwordInput = "input-password",
  loginButton = "button-login",
  logoutButton = "button-logout",

  // Account Editing

  accountPage = "page-account",
  passwordCurrentInput = "input-current-password",
  passwordNewInput = "input-new-password",
  passwordChangeButton = "button-update-password",
  accountDeletePasswordInput = "input-delete-password",
  accountDeleteButton = "button-delete-my-account",
  popUpAcceptButton = "button-confirm-modal",

  // Snackbar

  snackbarInfo = "snackbar-info",
  snackbarSuccess = "snackbar-success",
  snackbarWarning = "snackbar-warning",
  snackbarError = "snackbar-error",
  snackbarCloseButton = "button-snackbar-close",

  // Project Creation

  creationBulkNameInput = "input-project-name-bulk",
  creationBulkDescriptionInput = "input-project-description-bulk",
  creationBulkFilesInput = "input-files-bulk",
  creationEmptyToggle = "toggle-create-empty-project",
  creationTimToggle = "toggle-tim-manage",
  creationTimArtifactsInput = "input-tim-artifacts",
  creationTimTracesInput = "input-tim-traces",

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
  creationTraceSourceInput = "input-source-type",
  creationTraceTargetInput = "input-target-type",
  creationTraceCreateButton = "button-create-trace-matrix",

  // Jobs

  jobTable = "job-table",
  jobStatus = "job-status",
  jobPanel = "job-panel",
  jobDeleteButton = "button-delete-job",
  jobOpenButton = "button-open-job",

  // Project Selection

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
  traceSaveDirectionsPanel = "panel-trace-directions",
  traceSaveDirectionsChip = "chip-type-direction",
  traceSaveSubmitButton = "button-trace-save",

  traceApproveModal = "modal-trace-approve",
  traceUnreviewButton = "button-trace-unreview",
  traceApproveButton = "button-trace-approve",
  traceDeclineButton = "button-trace-decline",
  traceDeleteButton = "button-trace-delete",

  // Selection Panel

  selectedPanelName = "text-selected-name",
  selectedPanelType = "text-selected-type",
  selectedPanelBody = "text-selected-body",
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

  artifactTree = "view-artifact-tree",
  treeNode = "tree-node",
  treeNodeName = "tree-node-name",
  treeNodeType = "tree-node-type",
  treeNodeBody = "tree-node-body",
  treeSelectedNode = "tree-node-selected",

  // Artifact Search

  artifactSearchNavInput = "input-artifact-search-nav",
  artifactSearchSideInput = "input-artifact-search-side",
  artifactSearchCount = "text-artifact-search-count",
  artifactSearchTypeList = "list-artifact-search-type",
  artifactSearchItem = "text-artifact-search-item",

  // Type Options

  typeOptionsList = "list-type-options",
  typeOptionsIconButton = "button-type-options-icon",

  // Project settings

  projectSettingsAddEmail = "settings-input-user-email",
  projectSettingsAddRole = "settings-input-user-role",
  projectSettingsAddToProject = "button-add-user-to-project",
  projectSettingsEditUserButton = "button-selector-edit",
  projectSettingsDeleteUserButton = "button-selector-delete",
  projectSettingsIAcceptButton = "button-confirm-modal",
  projectSettingsSearchUser = "input-selector-search",
  projectSettingsTable = "generic-selector-table",

  // Project Documents

  documentSelectButton = "button-document-select-open",
  documentCreateButton = "button-document-select-create",
  documentItemButton = "button-document-select-item",
  documentEditButton = "button-document-select-edit",
  documentModal = "modal-document-save",
  documentNameInput = "input-document-name",
  documentTypeInput = "input-document-type",
  documentIncludeTypesInput = "input-document-include-types",
  documentArtifactsInput = "input-document-artifacts",
  documentIncludeChildrenToggle = "button-document-include-children",
  documentChildTypesInput = "input-document-include-child-types",
  documentChildArtifactsInput = "input-document-child-artifacts",
  documentDeleteButton = "button-document-delete",
  documentSaveTypesButton = "button-save-types",
  documentSaveArtifactsButton = "button-save-artifacts",
  documentSaveButton = "button-document-save",

  // Artifact Table
  artifactTable = "view-artifact-table",
  artifactTableRow = "table-row-artifact",
  artifactTableSortBy = "artifact-table-sort-by",
  artifactTableGroupBy = "artifact-table-group-by",
  artifactTableGroupByTableHeader = "artifact-table-group-sort-header",
  artifactTableListItems = "button-checkmark-menu-item",
  artifactTableColumnHeader = "artifact-table-column-header",
  artifactTableNameHeaderNotSorted = '*[aria-label= "Name: Not sorted. Activate to sort ascending."][aria-sort= "none"]',
  artifactTableTypeHeaderNotSorted = '*[aria-label= "Type: Not sorted. Activate to sort ascending."][aria-sort= "none"]',
  artifactTableNameHeaderSortedAsc = '*[aria-label= "Name: Sorted ascending. Activate to sort descending."][aria-sort= "ascending"]',
  artifactTableTypeHeaderSortedAsc = '*[aria-label= "Type: Sorted ascending. Activate to sort descending."][aria-sort= "ascending"]',
  artifactTableArtifact = "artifact-table-artifact",
  artifactTableArtifactWarning = "artifact-table-artifact-warning",
  artifactTableArtifactWarningLabel = "artifact-table-panel-warnings-title",

  // Artifact Table - Create New Artifact
  artifactTableAddContentButton = "button-fab-toggle",
  artifactTableAddArtifactButton = "button-fab-create-artifact",
  artifactTableCreateArtifactNameInput = "input-artifact-name",
  artifactTableCreateArtifactTypeInput = "input-artifact-type",
  artifactTableCreateArtifactDocumentTypeInput = "input-artifact-document",
  artifactTableCreateArtifactParentArtifactInput = "input-artifact-parent",
  artifactTableCreateArtifactBodyInput = "input-artifact-body",
  artifactTableCreateArtifactSummaryInput = "input-artifact-summary",
  artifactTableCreateArtifactSaveButton = "button-artifact-save",
  artifactTableEditArtifactRowButton = "button-artifact-edit-icon",
  artifactTableDeleteArtifactRowButton = "button-artifact-delete-icon",
  artifactTableArtifactPanelBody = "text-selected-body",
  artifactTableArtifactDeleteIAcceptButton = "button-confirm-modal",

  // Trace Link Generation
  traceLinkTable = "table-trace-link",
  traceLinkTableGenerateTraceLinkApproveButton = "button-trace-link-generate-approve",
  traceLinkTableGenerateTraceLinkDeclineButton = "button-trace-link-generate-decline",
  traceLinkTableGenerateTraceLinkUnapproveButton = "button-trace-link-generate-unapproved",
  traceLinkTableApprovalTypeButton = "button-trace-link-generate-approval-type",
  traceLinkTableSortByInput = "artifact-table-sort-by",
  traceLinkTableGroupByInput = "artifact-table-group-by",
}

export enum DataIds {
  rightClickAddArtifact = "#add-artifact",
  rightClickDuplicateArtifact = "#duplicate-artifact",
  rightClickHideSubtree = "#hide-subtree",
  rightClickShowSubtree = "#show-subtree",
}
