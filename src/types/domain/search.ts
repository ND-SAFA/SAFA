/**
 * Represents a request to search for matching artifacts within a project.
 */
export interface ProjectSearchQuerySchema {
  /**
   * The type of information to predict traces to.
   */
  mode: "prompt" | "artifacts" | "artifactTypes";
  /**
   * Used in "prompt" mode.
   * This string of text will be treated as an artifact to predict links from.
   */
  prompt?: string;
  /**
   * Used in "artifacts" mode.
   * These artifacts will be used as the base to predict links from.
   */
  artifactIds?: string[];
  /**
   * Used in "artifactTypes" mode.
   * All artifacts of these types will be used as the base to predict links from.
   */
  artifactTypes?: string[];

  /**
   * What type(s) of artifacts to predict links from the search artifacts to.
   */
  searchTypes: string[];
  /**
   * The model to predict links with.
   * @default Our best model.
   */
  model?: string;
  /**
   * How many of the top predictions to include.
   * @default 5
   */
  maxResults?: number;
  /**
   * What other type(s) of artifacts should I import,
   * if they have existing links to the artifacts retrieved with the search artifacts + `searchTypes` artifacts.
   */
  relatedTypes?: string[];
}
