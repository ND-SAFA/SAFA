import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

import type {
  LinkFinder,
  LinkValidator,
  TraceLink,
  DocumentTraces,
} from "@/types";
import { TraceApproval } from "@/types";
import { documentModule } from "@/store";
import { getTraceId } from "@/util";

@Module({ namespaced: true, name: "trace" })
/**
 * This module defines the state of the currently visible trace links.
 */
export default class TraceModule extends VuexModule {
  /**
   * All trace links in the project.
   */
  private projectTraces: TraceLink[] = [];
  /**
   * The trace links visible artifacts.
   */
  private currentTraces: TraceLink[] = [];

  @Action
  /**
   * Initializes the trace links visible in the current document.
   */
  initializeTraces(documentTraces: DocumentTraces): void {
    const { traces = this.projectTraces, currentArtifactIds } = documentTraces;

    this.SET_PROJECT_TRACES(traces);
    this.SET_CURRENT_TRACES(
      currentArtifactIds
        ? traces.filter(
            ({ sourceId, targetId }) =>
              currentArtifactIds.includes(sourceId) &&
              currentArtifactIds.includes(targetId)
          )
        : traces
    );
  }

  @Action
  /**
   * Updates the current trace links in the project, preserving any that already existed.
   *
   * @param traceLinks - The trace links to set.
   */
  async addOrUpdateTraceLinks(updatedTraces: TraceLink[]): Promise<void> {
    const visibleIds = documentModule.document.artifactIds;
    const visibleTraces = updatedTraces.filter(
      ({ sourceId, targetId }) =>
        visibleIds.includes(sourceId) && visibleIds.includes(targetId)
    );

    this.SET_PROJECT_TRACES(updatedTraces);
    this.SET_CURRENT_TRACES(visibleTraces);
  }

  @Action
  /**
   * Deletes the given trace link.
   *
   * @param traceLink - The trace link to remove.
   */
  async deleteTraceLinks(traceLinks: TraceLink[]): Promise<void> {
    const deletedIds = traceLinks.map(({ traceLinkId }) => traceLinkId);
    const removeLink = (currentTraces: TraceLink[]) =>
      currentTraces.filter(
        ({ traceLinkId }) => !deletedIds.includes(traceLinkId)
      );

    this.SET_PROJECT_TRACES(removeLink(this.projectTraces));
    this.SET_CURRENT_TRACES(removeLink(this.currentTraces));
  }

  @Mutation
  /**
   * Sets the project trace links.
   */
  SET_PROJECT_TRACES(traces: TraceLink[]): void {
    this.projectTraces = traces;
  }

  @Mutation
  /**
   * Sets the current trace links.
   */
  SET_CURRENT_TRACES(traces: TraceLink[]): void {
    this.currentTraces = traces;
  }

  /**
   * @return All trace links in the project.
   */
  get allTraces(): TraceLink[] {
    return this.projectTraces;
  }

  /**
   * @return The trace links for the current document.
   */
  get traces(): TraceLink[] {
    return this.currentTraces;
  }

  /**
   * @return All non-declined trace links.
   */
  get nonDeclinedTraces(): TraceLink[] {
    return this.currentTraces.filter(
      (t) => t.approvalStatus != TraceApproval.DECLINED
    );
  }

  /**
   * @return Returns a function to query a single trace link by the
   * source and target artifact ids.
   */
  get getTraceLinkByArtifacts(): LinkFinder {
    return (sourceId, targetId) => {
      const traceQuery = this.traces.filter(
        (trace) => trace.sourceId === sourceId && trace.targetId === targetId
      );

      if (traceQuery.length === 0) {
        throw Error(
          `Could not find trace link with id: ${getTraceId(sourceId, targetId)}`
        );
      }

      return traceQuery[0];
    };
  }

  /**
   * @return A function that determines whether a link with the given source and target IDs exists.
   */
  get doesLinkExist(): LinkValidator {
    return (sourceId, targetId) => {
      const traceLinkQuery = this.traces.filter(
        (trace) =>
          (trace.sourceId === sourceId && trace.targetId === targetId) ||
          (trace.targetId === sourceId && trace.sourceId === targetId)
      );

      return traceLinkQuery.length > 0;
    };
  }
}
