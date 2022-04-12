import {
  Artifact,
  ArtifactType,
  ColumnDataType,
  Commit,
  ConfirmationType,
  ConfirmDialogueMessage,
  DocumentColumn,
  DocumentType,
  FTANodeType,
  MessageType,
  Project,
  ProjectDelta,
  ProjectDocument,
  ProjectIdentifier,
  ProjectVersion,
  SafetyCaseType,
  SessionModel,
  SnackbarMessage,
} from "@/types";

/**
 * @return An empty snackbar message.
 */
export function createSnackbarMessage(): SnackbarMessage {
  return {
    errors: [],
    message: "",
    type: MessageType.CLEAR,
  };
}

/**
 * @return An empty confirm dialog message.
 */
export function createConfirmDialogueMessage(): ConfirmDialogueMessage {
  return {
    type: ConfirmationType.CLEAR,
    title: "",
    body: "",
    statusCallback: () => null,
  };
}

/**
 * @return An empty session.
 */
export function createSession(): SessionModel {
  return {
    token: "",
    versionId: "",
  };
}

/**
 * @return An empty project identifier.
 */
export function createProjectIdentifier(
  identifier?: Partial<ProjectIdentifier>
): ProjectIdentifier {
  return {
    name: identifier?.name || "",
    projectId: identifier?.projectId || "",
    description: identifier?.description || "",
    owner: identifier?.owner || "",
    members: identifier?.members || [],
  };
}

/**
 * @return An empty project.
 */
export function createProject(project?: Partial<Project>): Project {
  return {
    ...createProjectIdentifier(project),
    artifacts: project?.artifacts || [],
    traces: project?.traces || [],
    projectVersion: project?.projectVersion || undefined,
    artifactTypes: project?.artifactTypes || [],
    documents: project?.documents || [],
  };
}

/**
 * @return An empty project delta.
 */
export function createProjectDelta(): ProjectDelta {
  return {
    artifacts: {
      added: {},
      modified: {},
      removed: {},
    },
    traces: {
      added: {},
      modified: {},
      removed: {},
    },
  };
}

/**
 * @return An artifact initialized to the given props.
 */
export function createArtifact(artifact?: Partial<Artifact>): Artifact {
  return {
    id: artifact?.id || "",
    name: artifact?.name || "",
    summary: artifact?.summary || "",
    body: artifact?.body || "",
    type: artifact?.type || "",
    documentType: artifact?.documentType || DocumentType.ARTIFACT_TREE,
    documentIds: artifact?.documentIds || [],
    safetyCaseType: artifact?.safetyCaseType || SafetyCaseType.GOAL,
    logicType: artifact?.logicType || FTANodeType.AND,
    customFields: artifact?.customFields || {},
  };
}

/**
 * @return An column initialized to the given props.
 */
export function createColumn(column?: Partial<DocumentColumn>): DocumentColumn {
  return {
    id: column?.id || "",
    name: column?.name || "",
    dataType: column?.dataType || ColumnDataType.FREE_TEXT,
    required: column?.required || false,
  };
}

/**
 * @returns An empty commit.
 */
export function createCommit(version: ProjectVersion): Commit {
  return {
    commitVersion: version,
    artifacts: {
      added: [],
      removed: [],
      modified: [],
    },
    traces: {
      added: [],
      removed: [],
      modified: [],
    },
  };
}

/**
 * @returns A record mapping the lowercase artifact type name to the corresponding default icon.
 */
export function createDefaultTypeIcons(
  artifactTypes: ArtifactType[] = []
): Record<string, string> {
  return artifactTypes
    .map((t) => ({ [t.name]: t.icon }))
    .reduce((acc, cur) => ({ ...acc, ...cur }), { default: "mdi-help" });
}

/**
 * @return An document initialized to the given props.
 */
export function createDocument(
  document?: Partial<ProjectDocument>
): ProjectDocument {
  return {
    documentId: document?.documentId || "",
    project: document?.project || {
      projectId: "",
      name: "",
      description: "",
      owner: "",
      members: [],
    },
    name: document?.name || "Default",
    type: document?.type || DocumentType.ARTIFACT_TREE,
    artifactIds: document?.artifactIds || [],
    description: document?.description || "",
  };
}
