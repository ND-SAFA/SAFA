import {
  ArtifactModel,
  ArtifactTypeModel,
  DocumentModel,
  LayoutPositionsModel,
  MembershipModel,
  TraceLinkModel,
  GenerationModel,
  WarningModel,
  AttributeModel,
  AttributeLayoutModel,
} from "@/types";

/**
 * Defines a project.
 */
export interface IdentifierModel {
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
  members: MembershipModel[];

  /**
   * The primary owner of this project.
   */
  owner: string;
}

/**
 * Defines the version of a project.
 */
export interface VersionModel {
  /**
   * The project version id.
   */
  versionId: string;
  /**
   * The project.
   */
  project?: IdentifierModel;
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
export interface ProjectModel extends IdentifierModel {
  /**
   * The project's version.
   */
  projectVersion?: VersionModel;

  /**
   * The project's artifacts.
   */
  artifacts: ArtifactModel[];
  /**
   * The project's traces.
   */
  traces: TraceLinkModel[];
  /**
   * The artifact types present in the project.
   */
  artifactTypes: ArtifactTypeModel[];

  /**
   * The current document id.
   */
  currentDocumentId?: string;
  /**
   * The different documents for this project.
   */
  documents: DocumentModel[];

  /**
   * A collection of warnings on project artifacts.
   */
  warnings: Record<string, WarningModel[]>;

  /**
   * Map of artifact ids to their position in the default graph.
   */
  layout: LayoutPositionsModel;

  /**
   * List of trained project models.
   */
  models: GenerationModel[];

  /**
   * A list of custom attributes used on this project.
   */
  attributes?: AttributeModel[];
  /**
   * Layouts for displaying this project's custom attributes.
   */
  attributeLayouts?: AttributeLayoutModel[];
}

export type VersionType = "major" | "minor" | "revision";
