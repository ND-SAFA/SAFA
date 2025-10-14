import { ComputedRef, Ref } from "vue";
import {
  ArtifactCytoElementData,
  ArtifactSchema,
  IOHandlerCallback,
  TraceLinkSchema,
} from "@/types";

/**
 * A hook for calling trace link API endpoints.
 */
export interface TraceApiHook {
  /**
   * The ids of any trace links currently loading
   * approval status changes.
   */
  loadingTraceIds: Ref<string[]>;
  /**
   * Whether the create request is loading.
   */
  createLoading: ComputedRef<boolean>;
  /**
   * Whether the edit request is loading.
   */
  editLoading: ComputedRef<boolean>;
  /**
   * Whether the approval request is loading.
   */
  approveLoading: ComputedRef<boolean>;
  /**
   * Whether the decline request is loading.
   */
  declineLoading: ComputedRef<boolean>;
  /**
   * Whether the unreview request is loading.
   */
  unreviewLoading: ComputedRef<boolean>;
  /**
   * Creates a new trace link.
   *
   * @param source - The artifact to link from.
   * @param target - The artifact to link to.
   * @param explanation - The explanation for the trace link.
   * @param callbacks - The callbacks to call after the action.
   */
  handleCreate(
    source: ArtifactSchema | ArtifactCytoElementData,
    target: ArtifactSchema | ArtifactCytoElementData,
    explanation?: string,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  /**
   * Creates a new trace link between all source to all target artifacts in the saved trace store.
   */
  handleCreateAll(): Promise<void>;
  /**
   * Processes link approvals, setting the app state to loading in between, and updating trace links afterwards.
   *
   * @param traceLink - The trace link to process.
   * @param callbacks - The callbacks to call after the action.
   */
  handleApprove(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void>;
  /**
   * Processes link declines, setting the app state to loading in between, and updating trace links afterwards.
   *
   * @param traceLink - The trace link to process.
   * @param callbacks - The callbacks to call after the action.
   */
  handleDecline(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void>;
  /**
   * Declines all unreviewed links, setting the app state to loading in between, and updating trace links.
   */
  handleDeclineAll(): Promise<void>;
  /**
   * Processes link unreview, setting the app state to loading in between, and updating trace links afterwards.
   *
   * @param traceLink - The trace link to process.
   * @param callbacks - The callbacks to call after the action.
   */
  handleUnreview(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void>;
  /**
   * Edits an existing trace link.
   *
   * @param traceLink - The trace link to edit.
   * @param callbacks - The callbacks to call after the action.
   */
  handleEdit(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void>;
  /**
   * Deletes a trace link after confirmation.
   *
   * @param traceLink - The trace link to delete.
   * @param callbacks - The callbacks to call after the action.
   */
  handleDelete(
    traceLink: TraceLinkSchema,
    callbacks: IOHandlerCallback
  ): Promise<void>;
}
