import {
  ArtifactSchema,
  ArtifactTypeSchema,
  DocumentSchema,
  LayoutPositionsSchema,
  MembershipSchema,
  TraceLinkSchema,
  GenerationModelSchema,
  WarningSchema,
  AttributeSchema,
  AttributeLayoutSchema,
} from "@/types";

/**
 * Defines a project.
 */
export interface IdentifierSchema {
  /**
   * The ID of the project.
   */
  projectId: string;

  /**
   * The name of the project.
   */
  name: string;
  /**
   * The description of the project.
   */
  description: string;

  /**
   * List of members and their roles in the project.
   */
  members: MembershipSchema[];

  /**
   * The primary owner of this project.
   */
  owner: string;
}

/**
 * Defines the version of a project.
 */
export interface VersionSchema {
  /**
   * The project version id.
   */
  versionId: string;
  /**
   * The project.
   */
  project?: IdentifierSchema;
  /**
   * The major version number.
   */
  majorVersion: number;
  /**
   * The minor version number.
   */
  minorVersion: number;
  /**
   * The revision version number.
   */
  revision: number;
}

/**
 * Defines a versioned and parsed project.
 */
export interface ProjectSchema extends IdentifierSchema {
  /**
   * The project's version.
   */
  projectVersion?: VersionSchema;

  /**
   * The project's artifacts.
   */
  artifacts: ArtifactSchema[];
  /**
   * The project's traces.
   */
  traces: TraceLinkSchema[];
  /**
   * The artifact types present in the project.
   */
  artifactTypes: ArtifactTypeSchema[];

  /**
   * The current document id.
   */
  currentDocumentId?: string;
  /**
   * The different documents for this project.
   */
  documents: DocumentSchema[];

  /**
   * A collection of warnings on project artifacts.
   */
  warnings: Record<string, WarningSchema[]>;

  /**
   * Map of artifact ids to their position in the default graph.
   */
  layout: LayoutPositionsSchema;

  /**
   * List of trained project models.
   */
  models: GenerationModelSchema[];

  /**
   * A list of custom attributes used on this project.
   */
  attributes?: AttributeSchema[];
  /**
   * Layouts for displaying this project's custom attributes.
   */
  attributeLayouts?: AttributeLayoutSchema[];
}

export type VersionType = "major" | "minor" | "revision";
