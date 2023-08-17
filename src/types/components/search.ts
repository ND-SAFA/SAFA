import { ArtifactSchema } from "@/types";

/**
 * The props for rendering a search list item.
 */
export interface SearchOptionProps {
  /**
   * The option to display, either an artifact or artifact type.
   */
  option: ArtifactSchema | string;
}
