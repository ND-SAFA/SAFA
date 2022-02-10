import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";

import type { TraceLink, LinkFinder, LinkValidator } from "@/types";
import { DocumentTraces } from "@/types";
import { subtreeModule } from "@/store";
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
  async addOrUpdateTraceLinks(newTraces: TraceLink[]): Promise<void> {
    const newIds = newTraces.map(({ traceLinkId }) => traceLinkId);
    const createNewLinks = (currentTraces: TraceLink[]) => [
      ...currentTraces.filter(
        ({ traceLinkId }) => !newIds.includes(traceLinkId)
      ),
      ...newTraces,
    ];

    this.SET_PROJECT_TRACES(createNewLinks(this.projectTraces));
    this.SET_CURRENT_TRACES(createNewLinks(this.currentTraces));

    await subtreeModule.updateSubtreeMap();
  }

  @Action
  /**
   * Deletes the given trace link.
   *
   * @param traceLink - The trace link to remove.
   */
  async deleteTraceLink(traceLink: TraceLink): Promise<void> {
    const removeLink = (currentTraces: TraceLink[]) =>
      currentTraces.filter(
        ({ traceLinkId }) => traceLinkId !== traceLink.traceLinkId
      );

    this.SET_PROJECT_TRACES(removeLink(this.projectTraces));
    this.SET_CURRENT_TRACES(removeLink(this.currentTraces));

    await subtreeModule.updateSubtreeMap();
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
