import { Ref } from "vue";
import { IOHandlerCallback, VersionSchema } from "@/types";

/**
 * A hook for calling delta API endpoints.
 */
export interface DeltaApiHook {
  /**
   * Whether the request is loading.
   */
  loading: Ref<boolean>;
  /**
   * The versions of the current project that delta can be performed against.
   */
  deltaVersions: Ref<VersionSchema[]>;
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
}
