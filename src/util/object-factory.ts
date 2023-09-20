import {
  ArtifactSchema,
  CommitSchema,
  ConfirmDialogueMessage,
  DocumentSchema,
  FTANodeType,
  IdentifierSchema,
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
  AttributeLayoutSchema,
  MatrixSchema,
  GeneratedMatrixSchema,
  OrganizationSchema,
  TeamSchema,
  TraceLinkSchema,
} from "@/types";

export function buildSnackbarMessage(): SnackbarMessage {
  return {
    errors: [],
    message: "",
    type: "clear",
  };
}

export function buildConfirmMessage(): ConfirmDialogueMessage {
  return {
    type: "clear",
    title: "",
    body: "",
    statusCallback: () => null,
  };
}

export function buildUser(): UserSchema {
  return {
    userId: "",
    email: "",
    personalOrgId: "",
    defaultOrgId: "",
    superuser: false,
  };
}

export function buildSession(): SessionSchema {
  return {
    token: "",
    versionId: "",
  };
}

export function buildProjectIdentifier(
  identifier?: Partial<IdentifierSchema>
): IdentifierSchema {
  return {
    name: identifier?.name || "",
    projectId: identifier?.projectId || "",
    orgId: identifier?.orgId || "",
    teamId: identifier?.teamId || "",
    description: identifier?.description || "",
    owner: identifier?.owner || "",
    members: identifier?.members || [],
  };
}

export function buildProject(project?: Partial<ProjectSchema>): ProjectSchema {
  return {
    ...buildProjectIdentifier(project),
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

export function buildProjectDelta(): VersionDeltaSchema {
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

export function buildTraceLink(
  trace?: Partial<TraceLinkSchema>
): TraceLinkSchema {
  return {
    traceLinkId: trace?.traceLinkId || "",
    sourceId: trace?.sourceId || "",
    sourceName: trace?.sourceName || "",
    targetId: trace?.targetId || "",
    targetName: trace?.targetName || "",
    approvalStatus: trace?.approvalStatus || "UNREVIEWED",
    score: trace?.score || 1,
    traceType: trace?.traceType || "MANUAL",
    explanation: trace?.explanation || "",
  };
}

export function buildArtifact(
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
    documentType: artifact?.documentType || "ARTIFACT_TREE",
    documentIds: artifact?.documentIds || [],
    safetyCaseType: artifact?.safetyCaseType || "GOAL",
    logicType: artifact?.logicType || "AND",
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
export function buildArtifactOfType(
  artifact: Partial<ArtifactSchema> | undefined,
  type?: true | string
): ArtifactSchema {
  if (typeof type === "string") {
    const isFTA = type in (["AND", "OR"] as FTANodeType[]);
    const isSC =
      type in (["GOAL", "SOLUTION", "STRATEGY", "CONTEXT"] as SafetyCaseType[]);

    if (isFTA || type === "FTA") {
      return buildArtifact({
        ...artifact,
        documentType: "FTA",
        logicType: isFTA ? (type as FTANodeType) : "AND",
        type: "FTA",
      });
    } else if (isSC) {
      return buildArtifact({
        ...artifact,
        documentType: "SAFETY_CASE",
        safetyCaseType: isSC ? (type as SafetyCaseType) : "CONTEXT",
        type: "SAFETY_CASE",
      });
    } else if (type === "FMEA") {
      return buildArtifact({
        ...artifact,
        documentType: "FMEA",
        type: "FMEA",
      });
    }
  }

  return buildArtifact(artifact);
}

export function buildCommit(version: VersionSchema): CommitSchema {
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

export function buildDocument(
  document?: Partial<DocumentSchema>
): DocumentSchema {
  return {
    documentId: document?.documentId || "",
    project: document?.project || buildProjectIdentifier(),
    name: document?.name || "",
    type: document?.type || "ARTIFACT_TREE",
    artifactIds: document?.artifactIds || [],
    description: document?.description || "",
    layout: document?.layout || {},
  };
}

export function buildModel(
  model?: Partial<GenerationModelSchema>
): GenerationModelSchema {
  return {
    id: model?.id || "",
    name: model?.name || "",
    baseModel: model?.baseModel || "NLBert",
  };
}

export function buildAttribute(
  attribute?: Partial<AttributeSchema>
): AttributeSchema {
  return {
    key: attribute?.key || "",
    label: attribute?.label || "",
    type: attribute?.type || "text",
    options: attribute?.options,
    min: attribute?.min,
    max: attribute?.max,
  };
}

export function buildAttributeLayout(
  layout?: Partial<AttributeLayoutSchema>
): AttributeLayoutSchema {
  return {
    id: layout?.id || "",
    name: layout?.name || "",
    artifactTypes: layout?.artifactTypes || [],
    positions: layout?.positions?.map((pos) => ({ ...pos })) || [],
  };
}

export function buildGeneratedMatrix(
  artifactLevels: MatrixSchema[],
  method?: ModelType,
  model?: GenerationModelSchema
): GeneratedMatrixSchema {
  return {
    method: model?.baseModel || method || undefined,
    model,
    artifactLevels: artifactLevels,
  };
}

export function buildOrg(
  org: Partial<OrganizationSchema> = {}
): OrganizationSchema {
  return {
    id: org.id || "",
    name: org.name || "",
    description: org.description || "",
    personalOrg: org.personalOrg || false,
    paymentTier: org.paymentTier || "",
    members: org.members || [],
    teams: org.teams || [],
  };
}

export function buildTeam(team: Partial<TeamSchema> = {}): TeamSchema {
  return {
    id: team.id || "",
    name: team.name || "",
    members: team.members || [],
    projects: team.projects || [],
  };
}
