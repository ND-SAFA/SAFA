import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";

import type { TraceLink, DocumentTraces } from "@/types";

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
    const { traces, currentArtifactIds } = documentTraces;

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
}
