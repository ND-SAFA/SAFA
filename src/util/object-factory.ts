import {
  ArtifactSchema,
  CommitSchema,
  ConfirmationType,
  ConfirmDialogueMessage,
  DocumentSchema,
  DocumentType,
  FTANodeType,
  IdentifierSchema,
  MessageType,
  ModelType,
  VersionDeltaSchema,
  ProjectSchema,
  SafetyCaseType,
  SessionSchema,
  SnackbarMessage,
  GenerationModelSchema,
  UserSchema,
  VersionSchema,
  AttributeSchema,
  AttributeType,
  AttributeLayoutSchema,
  ArtifactLevelSchema,
  GeneratedMatrixSchema,
} from "@/types";

/**
 * @return An empty snackbar message.
 */
export function createSnackbarMessage(): SnackbarMessage {
  return {
    errors: [],
    message: "",
    type: MessageType.clear,
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
 * @return An empty user.
 */
export function createUser(): UserSchema {
  return {
    userId: "",
    email: "",
  };
}

/**
 * @return An empty session.
 */
export function createSession(): SessionSchema {
  return {
    token: "",
    versionId: "",
  };
}

/**
 * @return A project identifier initialized to the given values.
 */
export function createProjectIdentifier(
  identifier?: Partial<IdentifierSchema>
): IdentifierSchema {
  return {
    name: identifier?.name || "",
    projectId: identifier?.projectId || "",
    description: identifier?.description || "",
    owner: identifier?.owner || "",
    members: identifier?.members || [],
  };
}

/**
 * @return A project initialized to the given values.
 */
export function createProject(project?: Partial<ProjectSchema>): ProjectSchema {
  return {
    ...createProjectIdentifier(project),
    artifacts: project?.artifacts || [],
    traces: project?.traces || [],
    projectVersion: project?.projectVersion,
    artifactTypes: project?.artifactTypes || [],
    traceMatrices: project?.traceMatrices || [],
    documents: project?.documents || [],
    warnings: project?.warnings || {},
    layout: project?.layout || {},
    subtrees: project?.subtrees || {},
    models: project?.models || [],
    attributes: project?.attributes || [],
    attributeLayouts: project?.attributeLayouts || [],
  };
}

/**
 * @return An empty project delta.
 */
export function createProjectDelta(): VersionDeltaSchema {
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
export function createArtifact(
  artifact?: Partial<ArtifactSchema>
): ArtifactSchema {
  return {
    id: artifact?.id || "",
    baseEntityId: artifact?.baseEntityId || "",
    name: artifact?.name || "",
    summary: artifact?.summary || "",
    body: artifact?.body || "",
    type: artifact?.type || "",
    isCode: artifact?.isCode || false,
    documentType: artifact?.documentType || DocumentType.ARTIFACT_TREE,
    documentIds: artifact?.documentIds || [],
    safetyCaseType: artifact?.safetyCaseType || SafetyCaseType.GOAL,
    logicType: artifact?.logicType || FTANodeType.AND,
    attributes: artifact?.attributes || {},
  };
}

/**
 * Creates an artifact that may be initialized to a specific document type.
 *
 * @param artifact - The base artifact to create from.
 * @param type - If true or matching no values, a normal artifact will be created.
 *               If equal to an `FTANodeType`, an FTA node will be created.
 *               If equal to a `SafetyCaseType`, a safety case node will be created.
 *               If equal to a `DocumentType.FMEA`, an FMEA node will be created.
 * @return An artifact initialized to the given props.
 */
export function createArtifactOfType(
  artifact: Partial<ArtifactSchema> | undefined,
  type?: true | string
): ArtifactSchema {
  if (typeof type === "string") {
    const isFTA = type in FTANodeType;
    const isSC = type in SafetyCaseType;

    if (isFTA || type === DocumentType.FTA) {
      return createArtifact({
        ...artifact,
        documentType: DocumentType.FTA,
        logicType: isFTA ? (type as FTANodeType) : FTANodeType.AND,
        type: DocumentType.FTA,
      });
    } else if (isSC) {
      return createArtifact({
        ...artifact,
        documentType: DocumentType.SAFETY_CASE,
        safetyCaseType: isSC
          ? (type as SafetyCaseType)
          : SafetyCaseType.CONTEXT,
        type: DocumentType.SAFETY_CASE,
      });
    } else if (type === DocumentType.FMEA) {
      return createArtifact({
        ...artifact,
        documentType: DocumentType.FMEA,
        type: DocumentType.FMEA,
      });
    }
  }

  return createArtifact(artifact);
}

/**
 * @returns An empty commit.
 */
export function createCommit(version: VersionSchema): CommitSchema {
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
 * @return An document initialized to the given props.
 */
export function createDocument(
  document?: Partial<DocumentSchema>
): DocumentSchema {
  return {
    documentId: document?.documentId || "",
    project: document?.project || {
      projectId: "",
      name: "",
      description: "",
      owner: "",
      members: [],
    },
    name: document?.name || "",
    type: document?.type || DocumentType.ARTIFACT_TREE,
    artifactIds: document?.artifactIds || [],
    description: document?.description || "",
    layout: document?.layout || {},
  };
}

/**
 * @return A model initialized to the given props.
 */
export function createModel(
  model?: Partial<GenerationModelSchema>
): GenerationModelSchema {
  return {
    id: model?.id || "",
    name: model?.name || "",
    baseModel: model?.baseModel || ModelType.NLBert,
  };
}

/**
 * @return An attribute initialized to the given props.
 */
export function createAttribute(
  attribute?: Partial<AttributeSchema>
): AttributeSchema {
  return {
    key: attribute?.key || "",
    label: attribute?.label || "",
    type: attribute?.type || AttributeType.text,
    options: attribute?.options,
    min: attribute?.min,
    max: attribute?.max,
  };
}

/**
 * @return An attribute layout initialized to the given props.
 */
export function createAttributeLayout(
  layout?: Partial<AttributeLayoutSchema>
): AttributeLayoutSchema {
  return {
    id: layout?.id || "",
    name: layout?.name || "",
    artifactTypes: layout?.artifactTypes || [],
    positions: layout?.positions?.map((pos) => ({ ...pos })) || [],
  };
}

/**
 * Creates a generated trace matrix defined over many artifact levels for
 * some tracing method or custom model.
 *
 * @param artifactLevels - The artifact levels to train on.
 * @param method - If a baseline method is used, this defines that method.
 * @param model - If a custom model is used,
 */
export function createGeneratedMatrix(
  artifactLevels: ArtifactLevelSchema[],
  method?: ModelType,
  model?: GenerationModelSchema
): GeneratedMatrixSchema {
  return {
    method: model?.baseModel || method || undefined,
    model,
    artifactLevels: artifactLevels,
  };
}
