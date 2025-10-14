import {
  ArtifactSchema,
  CommitSchema,
  ConfirmDialogueMessage,
  ViewSchema,
  IdentifierSchema,
  VersionDeltaSchema,
  ProjectSchema,
  SessionSchema,
  SnackbarMessage,
  UserSchema,
  VersionSchema,
  AttributeSchema,
  AttributeLayoutSchema,
  MatrixSchema,
  GeneratedMatrixSchema,
  OrganizationSchema,
  TeamSchema,
  TraceLinkSchema,
  UploadPanelType,
  CreatorFilePanel,
  ProjectChatSchema,
  ChatMessageSchema,
  MembershipSchema,
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

export function buildEmptyPanel(
  variant: UploadPanelType = "artifact"
): CreatorFilePanel {
  return {
    variant,
    name: "",
    type: "",
    open: true,
    valid: false,
    loading: false,
    ignoreErrors: false,
    itemNames: [],
    isGenerated: false,
    summarize: false,
    bulkFiles: [],
    emptyFiles: false,
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
    specification: identifier?.specification,
    owner: identifier?.owner || "",
    members: identifier?.members || [],
    permissions: identifier?.permissions || [],
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
    layout: project?.layout || {},
    subtrees: project?.subtrees || {},
    attributes: project?.attributes || [],
    attributeLayouts: project?.attributeLayouts || [],
    permissions: project?.permissions || [],
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
    documentIds: artifact?.documentIds || [],
    attributes: artifact?.attributes || {},
  };
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

export function buildDocument(document?: Partial<ViewSchema>): ViewSchema {
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
  artifactLevels: MatrixSchema[]
): GeneratedMatrixSchema {
  return {
    artifactLevels,
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
    members: org.members || [],
    teams: org.teams || [],
    permissions: org?.permissions || [],
    billing: {
      paymentTier: org?.billing?.paymentTier || "AS_NEEDED",
      totalUsedCredits: org?.billing?.totalUsedCredits || 0,
      totalSuccessfulCredits: org?.billing?.totalSuccessfulCredits || 0,
      monthlyUsedCredits: org?.billing?.monthlyUsedCredits || 0,
      monthlySuccessfulCredits: org?.billing?.monthlySuccessfulCredits || 0,
      monthlyRemainingCredits: org?.billing?.monthlyRemainingCredits || 0,
    },
  };
}

export function buildTeam(team: Partial<TeamSchema> = {}): TeamSchema {
  return {
    id: team.id || "",
    name: team.name || "",
    members: team.members || [],
    projects: team.projects || [],
    permissions: team?.permissions || [],
  };
}

export function buildMember(
  member: Partial<MembershipSchema> = {}
): MembershipSchema {
  return {
    id: member.id || "",
    email: member.email || "",
    role: member.role || "PENDING",
    entityType: member.entityType || "PROJECT",
    entityId: member.entityId || "",
  };
}

export function buildProjectChat(
  chat: Partial<ProjectChatSchema> = {}
): ProjectChatSchema {
  return {
    id: chat.id || "",
    title: chat.title || "New Chat",
    versionId: chat.versionId || "",
    permission: chat.permission || "owner",
    messages: chat.messages || [],
  };
}

export function buildProjectChatMessage(
  chat: Partial<ChatMessageSchema> = {}
): ChatMessageSchema {
  return {
    id: chat?.id || "",
    isUser: chat?.isUser === undefined ? true : chat.isUser,
    message: chat?.message || "",
    artifactIds: chat?.artifactIds || [],
    createdAt: chat?.createdAt || new Date().toISOString(),
  };
}
