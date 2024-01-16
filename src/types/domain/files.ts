import { MatrixSchema, ModelType, GenerationModelSchema } from "@/types/domain";

/**
 * Defines a trace matrix generation request.
 */
export interface GeneratedMatrixSchema {
  /**
   * The default model to use to generate links.
   */
  method?: ModelType;
  /**
   * The custom model used to generate links.
   */
  model?: GenerationModelSchema;
  /**
   * The artifact levels to trace with method.
   */
  artifactLevels: MatrixSchema[];
}

/**
 * Represents form data for uploading a project.
 */
export interface ProjectUploadFormData {
  name: string;
  orgId: string;
  teamId: string;
  description: string;
  summarize: boolean;
  files: File[];
}

/**
 * Represents form data for uploading a version.
 */
export interface VersionUploadFormData {
  asCompleteSet: boolean;
  files: File[];
}
