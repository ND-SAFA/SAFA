import { ArtifactProps, ArtifactSchema } from "@/types";

/**
 * The props for displaying an artifact name.
 */
export interface ArtifactNameDisplayProps extends ArtifactProps {
  /**
   * The artifact to display.
   */
  artifact: ArtifactSchema;
  /**
   * Whether to display the artifact type.
   */
  displayType?: boolean;
  /**
   * Whether to display the artifact name in a tooltip.
   */
  displayTooltip?: boolean;
  /**
   * Whether to display the name as a header.
   */
  isHeader?: boolean;
  /**
   * Whether to display the name more densely, such as on artifact nodes.
   */
  dense?: boolean;
  /**
   * Testing selector for the name.
   */
  dataCyName?: string;
  /**
   * Testing selector for the type.
   */
  dataCyType?: string;
  /**
   * The alignment of the name.
   */
  align?: "center" | "left" | "right";
}
