import { ProjectSchema } from "@/types";

/**
 * A hook for calling set project API endpoints.
 */
export interface SetProjectApiHook {
  /**
   * Clears project store data.
   */
  handleClear(): Promise<void>;
  /**
   * Sets a newly created project.
   *
   * @param project - Project created containing entities.
   */
  handleSet(project: ProjectSchema): Promise<void>;
}
