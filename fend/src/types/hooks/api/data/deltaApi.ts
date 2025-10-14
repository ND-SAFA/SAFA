import { ComputedRef } from "vue";
import { IOHandlerCallback, VersionSchema } from "@/types";

/**
 * A hook for calling delta API endpoints.
 */
export interface DeltaApiHook {
  /**
   * Whether the request is loading.
   */
  loading: ComputedRef<boolean>;
  /**
   * The versions of the current project that delta can be performed against.
   */
  deltaVersions: ComputedRef<VersionSchema[]>;
  /**
   * Sets a project delta.
   *
   * @param targetVersion - The target version of the project.
   * @param callbacks - Callbacks for the request.
   */
  handleCreate(
    targetVersion?: VersionSchema,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  /**
   * Disables delta mode and reloads the project.
   */
  handleDisable(): Promise<void>;
}
