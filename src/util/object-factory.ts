import {
  Commit,
  ConfirmationType,
  ConfirmDialogueMessage,
  DocumentType,
  MessageType,
  Project,
  ProjectDelta,
  ProjectDocument,
  ProjectVersion,
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
 * @return An empty project delta.
 */
export function createProject(): Project {
  return {
    name: "Untitled",
    projectId: "",
    description: "",
    members: [],
    artifacts: [],
    traces: [],
    projectVersion: undefined,
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
export function createDefaultTypeIcons(): Record<string, string> {
  return {
    requirement: "mdi-clipboard-text",
    design: "mdi-math-compass",
    hazard: "mdi-hazard-lights",
    environmentalassumption: "mdi-pine-tree-fire",
    default: "mdi-help",
  };
}

/**
 * @param artifactIds - The artifact ids visible in this document.
 * @return An empty document.
 */
export function createDocument(artifactIds: string[] = []): ProjectDocument {
  return {
    documentId: "",
    projectId: "",
    name: "Default",
    type: DocumentType.ARTIFACT_TREE,
    artifactIds,
  };
}
