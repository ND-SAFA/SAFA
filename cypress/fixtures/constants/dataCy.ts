/**
 * Represents all data cy selectors used in the app.
 */
export enum DataCy {
  // General

  appLoading = "app-loading",

  // Navigation - Project Graph

  navGraphCenterButton = "button-nav-graph-center",
  navGraphFilterButton = "button-nav-graph-filter",
  navGraphFilterOption = "button-checkmark-menu-item",
  navTreeButton = "button-nav-tree",
  navTableButton = "button-nav-table",
  navDeltaButton = "button-nav-delta",
  navTimButton = "button-nav-tim",
  sidebarCloseButton = "button-sidebar-close",
  navUndoButton = "button-nav-undo",
  navRedoButton = "button-nav-redo",
  navLoadUpdatesButton = "button-nav-load-update",

  // Navigation - Webpage
  navCreateProjectButton = "button-nav-Create Project",
  navOpenProjectButton = "button-nav-Open Project",
  navArtifactViewButton = "button-nav-Project View",
  navSettingsButton = "button-nav-Settings",

  // Steppers

  stepperContinueButton = "button-stepper-continue",
  stepperBackButton = "button-stepper-back",

  // Selector Tables

  selectorAddButton = "button-selector-add",
  selectorEditButton = "button-selector-edit",
  selectorDeleteButton = "button-selector-delete",
  selectorSearchInput = "input-selector-search",

  // Modals

  modalTitle = "modal-title",
  modalCloseButton = "button-close",
  confirmModalButton = "button-confirm-modal",

  // Account Creation

  newAccountEmailInput = "input-new-email",
  newAccountPasswordInput = "input-new-password",
  createAccountPageButton = "button-create-account-redirect",
  createAccountButton = "button-create-account",
  createAccountLoginButton = "button-create-account-login",

  // Authentication

  isLoggedIn = "is-logged-in",
  emailInput = "input-email",
  passwordInput = "input-password",
  loginButton = "button-login",
  logoutButton = "button-account-logout",

  // Account Editing

  accountPage = "icon-account",
  passwordCurrentInput = "input-current-password",
  passwordNewInput = "input-new-password",
  passwordChangeButton = "button-update-password",
  accountDeletePasswordInput = "input-delete-password",
  accountDeleteButton = "button-delete-my-account",

  // Snackbar

  snackbarInfo = "snackbar-info",
  snackbarSuccess = "snackbar-success",
  snackbarWarning = "snackbar-warning",
  snackbarUpdate = "snackbar-update",
  snackbarError = "snackbar-error",
  snackbarCloseButton = "button-snackbar-close",

  // Project Creation

  creationBulkNameInput = "input-project-name",
  creationBulkDescriptionInput = "input-project-description",
  creationBulkFilesInput = "input-files-bulk",
  creationEmptyToggle = "toggle-create-empty-project",
  creationTimToggle = "toggle-tim-manage",
  creationTimArtifactsInput = "input-tim-artifacts",
  creationTimTracesInput = "input-tim-traces",

  creationStandardNameInput = "input-project-name",
  creationStandardDescriptionInput = "input-project-description",
  creationStandardFilesInput = "input-files-panel",
  creationCreatePanelButton = "button-create-panel",
  creationTypeInput = "input-artifact-type",
  creationTypeButton = "button-artifact-type",
  creationArtifactDeleteButton = "button-delete-panel",
  creationEntitiesButton = "button-file-entities",
  creationIgnoreErrorsButton = "button-ignore-errors",
  creationDeletePanel = "button-delete-panel",
  creationFilePanel = "panel-files",
  creationContinueButton = "button-continue-project",
  creationUploadButton = "button-create-project",
  creationTraceSourceInput = "input-source-type",
  creationTraceTargetInput = "input-target-type",
  creationTraceCreateButton = "button-create-trace-matrix",

  // Jobs

  jobTable = "job-table",
  jobStatus = "job-status",
  jobProgress = "job-progress",
  jobPanel = "job-panel",
  jobDeleteButton = "button-delete-job",
  jobOpenButton = "button-open-job",
  jobLogButton = "button-job-log",
  jobLogText = "text-job-log",

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

  versionUploadFilesInput = "input-files-version",
  versionUploadFilesButton = "button-upload-files",

  // Artifact View

  artifactFabToggle = "button-fab-toggle",
  artifactFabCreateArtifact = "button-fab-create-artifact",
  artifactFabCreateTrace = "button-fab-create-trace",
  artifactFabDrawTrace = "button-fab-draw-trace",

  artifactSaveNameInput = "input-artifact-name",
  artifactSaveTypeInput = "input-artifact-type",
  artifactSaveBodyInput = "input-artifact-body",
  artifactSaveParentInput = "input-artifact-parent",
  artifactSaveSubmitButton = "button-artifact-save",

  traceSaveSourceInput = "button-trace-save-source",
  traceSaveTargetInput = "button-trace-save-target",
  traceSaveDirectionsPanel = "panel-trace-directions",
  traceSaveDirectionsChip = "chip-type-direction",
  traceSaveSubmitButton = "button-trace-save",

  traceUnreviewButton = "button-trace-unreview",
  traceApproveButton = "button-trace-approve",
  traceDeclineButton = "button-trace-decline",
  traceDeleteButton = "button-trace-delete",

  // Selection Panel

  selectedPanelCloseButton = "button-close-details",
  selectedPanelName = "text-selected-name",
  selectedPanelType = "text-selected-type",
  selectedPanelBody = "text-selected-body",
  selectedPanelBodyButton = "button-artifact-body",
  selectedPanelEditButton = "button-artifact-edit",
  selectedPanelDeleteButton = "button-artifact-delete",
  selectedPanelAttributePrefix = "text-attribute-",
  selectedPanelAttributeInputPrefix = "input-attribute-",

  selectedPanelParents = "list-selected-parents",
  selectedPanelParentItem = "list-selected-parent-item",
  selectedPanelParentLinkButton = "button-selected-parent-link",
  selectedPanelChildren = "list-selected-children",
  selectedPanelChildItem = "list-selected-child-item",
  selectedPanelChildLinkButton = "button-selected-child-link",

  selectedPanelTraceSource = "panel-trace-link-source",
  selectedPanelTraceTarget = "panel-trace-link-target",

  // Artifact Tree

  artifactTree = "view-artifact-tree",
  treeNode = "tree-node",
  treeNodeName = "tree-node-name",
  treeNodeType = "tree-node-type",
  treeSelectedNode = "tree-node-selected",

  // Artifact Search

  artifactSearchModeInput = "input-nav-search-mode",
  artifactSearchNavInput = "input-nav-artifact-search",
  artifactSearchCount = "text-artifact-search-count",
  artifactSearchItem = "text-artifact-search-item",

  // Type Options

  typeOptionsIconButton = "button-type-options-icon",
  artifactTypePanel = "panel-artifact-type",
  artifactTypeSavePanel = "panel-save-artifact-type",
  artifactLevelOptions = "panel-artifact-type-options",

  // Project settings

  projectSettingsDownloadButton = "button-settings-download",
  projectSettingsEditButton = "button-settings-edit",
  projectSettingsDeleteButton = "button-settings-delete",

  projectSettingsAddEmail = "input-member-email",
  projectSettingsAddRole = "input-member-role",
  projectSettingsSwitchRole = "button-member-role",
  projectSettingsAddToProject = "button-invite-member",
  projectSettingsDeleteUserButton = "button-selector-delete",
  projectSettingsTable = "generic-selector-table",

  // Project Documents

  documentSelectButton = "button-document-select-open",
  documentCreateButton = "button-document-select-create",
  documentItemButton = "button-document-select-item",
  documentEditButton = "button-document-select-edit",
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
  artifactTableRowName = "artifact-table-row-name",

  artifactTableSortByInput = "artifact-table-sort-by",
  artifactTableGroupByInput = "artifact-table-group-by",

  artifactTableGroup = "artifact-table-group",
  artifactTableGroupType = "artifact-table-group-type",
  artifactTableGroupValue = "artifact-table-group-value",

  artifactTableListItems = "button-checkmark-menu-item",
  artifactTableColumnHeader = "artifact-table-column-header",
  artifactTableDeleteArtifactButton = "button-artifact-delete-icon",

  artifactTableArtifactWarning = "artifact-table-artifact-warning",
  artifactTableArtifactWarningLabel = "artifact-table-panel-warnings-title",
  artifactTableEditArtifactRowButton = "button-artifact-edit-icon",

  // Trace Matrix Table

  traceMatrixTable = "view-trace-matrix-table",

  traceMatrixTableRowTypeInput = "input-trace-table-row-types",
  traceMatrixTableColTypeInput = "input-trace-table-col-types",

  // Trace Link Generation

  traceLinkTable = "table-trace-approval",
  traceLinkTableSortByInput = "artifact-table-sort-by",
  traceLinkTableGroupByInput = "artifact-table-group-by",
  traceLinkTableApprovalInput = "input-approval-type",

  // Project Version
  projectSavingIndicator = "project-saving-indicator",

  // Custom Attributes
  addAttributeButton = "button-add-attribute",
  attributeKeyInput = "input-attribute-key",
  attributeLabelInput = "input-attribute-label",
  attributeTypeInput = "input-attribute-type",
  attributeOptionsInput = "input-attribute-options",
  attributeMinInput = "input-attribute-min",
  attributeMaxInput = "input-attribute-max",
  attributeDeleteButton = "button-delete-attribute",
  attributeSaveButton = "button-save-attribute",
  attributeTableItem = "generic-list-item",

  attributeTableItemPlusButton = "button-add-attribute-to-layout",
  attributeLayoutAddButton = "button-attribute-layout-add",
  attributeLayoutNameInput = "input-attribute-layout-name",
  attributeLayoutTypeInput = "input-attribute-layout-artifact-types",
  attributeLayoutSaveButton = "button-attribute-layout-save",
  attributeLayoutDeleteAttributeButton = "button-attribute-layout-delete-attribute",
  attributeLayoutDeleteButton = "button-attribute-layout-delete",
  attributeLayoutConfirmDeleteButton = "button-confirm-modal",

  // Graph Menu
  rightClickAddArtifact = "button-add-artifact",
  rightClickAddTrace = "button-add-trace",
  rightClickToggleSubtree = "button-toggle-subtree",
}
