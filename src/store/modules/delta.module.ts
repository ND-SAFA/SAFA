import {
  AddedArtifact,
  RemovedArtifact,
  ModifiedArtifact,
} from "@/types/domain/delta";
import { ProjectVersion } from "@/types/domain/project";
import type { DeltaPayload } from "@/types/store";
import { PanelType } from "@/types/store";
import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";
import { appModule, projectModule } from "..";

@Module({ namespaced: true, name: "delta" })
export default class ErrorModule extends VuexModule {
  isDeltaViewEnabled = false;
  afterVersion: ProjectVersion | undefined = undefined;
  added: Record<string, AddedArtifact> = {};
  removed: Record<string, RemovedArtifact> = {};
  modified: Record<string, ModifiedArtifact> = {};

  @Action
  setIsDeltaViewEnabled(isDeltaViewEnabled: boolean): void {
    this.SET_DELTA_IN_VIEW(isDeltaViewEnabled);
  }

  @Action
  setDeltaPayload(payload: DeltaPayload): void {
    this.SET_DELTA_PAYLOAD(payload);
    projectModule.ADD_OR_UPDATE_ARTIFACTS(payload.missingArtifacts);
  }

  @Action
  setAfterVersion(payload: ProjectVersion | undefined): void {
    this.SET_AFTER_VERSION(payload);
  }

  @Action
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
  SET_DELTA_IN_VIEW(deltaInView: boolean): void {
    this.isDeltaViewEnabled = deltaInView;
  }
  @Mutation
  SET_DELTA_PAYLOAD(deltaPayload: DeltaPayload): void {
    this.added = deltaPayload.added;
    this.removed = deltaPayload.removed;
    this.modified = deltaPayload.modified;
  }
  @Mutation
  SET_AFTER_VERSION(afterVersion: ProjectVersion | undefined): void {
    this.afterVersion = afterVersion;
  }

  get getAdded(): Record<string, AddedArtifact> {
    return this.added;
  }
  get getRemoved(): Record<string, RemovedArtifact> {
    return this.removed;
  }
  get getModified(): Record<string, ModifiedArtifact> {
    return this.modified;
  }
  get getAfterVersion(): ProjectVersion | undefined {
    return this.afterVersion;
  }
  get getIsDeltaViewEnabled(): boolean {
    return this.isDeltaViewEnabled;
  }
}
