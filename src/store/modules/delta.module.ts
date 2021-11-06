import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";
import type {
  AddedArtifact,
  RemovedArtifact,
  ModifiedArtifact,
  ProjectVersion,
  DeltaPayload,
} from "@/types";
import { PanelType } from "@/types";
import { appModule, projectModule } from "..";

@Module({ namespaced: true, name: "delta" })
/**
 * This module defines state variables for tracking artifact deltas.
 */
export default class ErrorModule extends VuexModule {
  /**
   * Whether the artifact delta view is currently enabled.
   */
  private isDeltaViewEnabled = false;
  /**
   * The version that artifact deltas have been made to.
   */
  private afterVersion?: ProjectVersion;
  /**
   * A collection of all added artifacts.
   */
  private added: Record<string, AddedArtifact> = {};
  /**
   * A collection of all removed artifacts.
   */
  private removed: Record<string, RemovedArtifact> = {};
  /**
   * A collection of all modified artifacts.
   */
  private modified: Record<string, ModifiedArtifact> = {};

  @Action
  /**
   * Sets whether the delta view is enabled.
   *
   * @param isDeltaViewEnabled - Whether to enable this view.
   */
  setIsDeltaViewEnabled(isDeltaViewEnabled: boolean): void {
    this.SET_DELTA_IN_VIEW(isDeltaViewEnabled);
  }

  @Action
  /**
   * Sets the current artifact deltas.
   *
   * @param payload - All artifact deltas.
   */
  setDeltaPayload(payload: DeltaPayload): void {
    this.SET_DELTA_PAYLOAD(payload);
    projectModule.ADD_OR_UPDATE_ARTIFACTS(payload.missingArtifacts);
  }

  @Action
  /**
   * Sets the version that deltas are made to.
   *
   * @param version - The new version.
   */
  setAfterVersion(version?: ProjectVersion): void {
    this.SET_AFTER_VERSION(version);
  }

  @Action
  /**
   * Clears the current collections of artifact deltas.
   */
  clearDelta(): void {
    this.SET_DELTA_PAYLOAD({
      added: {},
      removed: {},
      modified: {},
      missingArtifacts: [],
    });
    this.SET_DELTA_IN_VIEW(false);
    appModule.closePanel(PanelType.right);
  }

  @Mutation
  /**
   * Sets whether the delta view is enabled.
   *
   * @param deltaInView - Whether to enable this view.
   */
  SET_DELTA_IN_VIEW(deltaInView: boolean): void {
    this.isDeltaViewEnabled = deltaInView;
  }

  @Mutation
  /**
   * Sets the current artifact deltas.
   *
   * @param deltaPayload - The collections of deltas to set.
   */
  SET_DELTA_PAYLOAD(deltaPayload: DeltaPayload): void {
    this.added = deltaPayload.added;
    this.removed = deltaPayload.removed;
    this.modified = deltaPayload.modified;
  }

  @Mutation
  /**
   * Sets the current version to apply deltas to.
   *
   * @param afterVersion - The new version.
   */
  SET_AFTER_VERSION(afterVersion?: ProjectVersion): void {
    this.afterVersion = afterVersion;
  }

  /**
   * @return A collection of added deltas.
   */
  get getAdded(): Record<string, AddedArtifact> {
    return this.added;
  }

  /**
   * @return A collection of removed deltas.
   */
  get getRemoved(): Record<string, RemovedArtifact> {
    return this.removed;
  }

  /**
   * @return A collection of modified deltas.
   */
  get getModified(): Record<string, ModifiedArtifact> {
    return this.modified;
  }

  /**
   * @return The current version that deltas are made to.
   */
  get getAfterVersion(): ProjectVersion | undefined {
    return this.afterVersion;
  }

  /**
   * @return Whether the delta view is currently enabled.
   */
  get getIsDeltaViewEnabled(): boolean {
    return this.isDeltaViewEnabled;
  }
}
