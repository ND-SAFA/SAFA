import {
  Commit,
  ConfirmationType,
  ConfirmDialogueMessage,
  MessageType,
  Project,
  ProjectDelta,
  ProjectVersion,
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
 * @return An empty project delta.
 */
export function createProject(): Project {
  return {
    name: "Untitled",
    projectId: "",
    description: "",
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
 * @return An empty commit.
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
