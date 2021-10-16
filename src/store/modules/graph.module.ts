import type { Artifact } from "@/types/domain/artifact";
import { appModule, viewportModule } from "@/store";
import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";
import {
  IgnoreTypeFilterAction,
  SubtreeFilterAction,
} from "@/cytoscape/filters/graph-filters";
import { PanelType } from "@/types/store";

export type FilterAction = IgnoreTypeFilterAction | SubtreeFilterAction;

export interface ChannelSubscriptionId {
  projectId?: string;
  versionId?: string;
}

@Module({ namespaced: true, name: "artifactSelection" })
export default class ArtifactSelectionModule extends VuexModule {
  selectedArtifact: Artifact | undefined = undefined;
  selectedSubtree: string[] = [];
  unselectedNodeOpacity = 0.1;
  ignoreTypes: string[] = [];

  @Action
  async filterGraph(filterAction: FilterAction): Promise<void> {
    switch (filterAction.type) {
      case "ignore":
        switch (filterAction.action) {
          case "add":
            return this.ADD_IGNORE_TYPE(filterAction.ignoreType);
          case "remove":
            return this.REMOVE_IGNORE_TYPE(filterAction.ignoreType);
        }
        break;
      case "subtree":
        this.SET_SELECTED_SUBTREE(filterAction.artifactsInSubtree);
        await viewportModule.repositionSelectedSubtree();
    }
  }

  @Action
  selectArtifact(artifact: Artifact): void {
    this.SELECT_ARTIFACT(artifact);
  }
  @Action
  unselectArtifact(): void {
    this.UNSELECT_ARTIFACT();
    appModule.closePanel(PanelType.left);
  }

  @Mutation
  SET_SELECTED_SUBTREE(artifacts: string[]): void {
    this.selectedSubtree = artifacts;
  }

  @Mutation
  ADD_IGNORE_TYPE(artifactTypeKey: string): void {
    this.ignoreTypes.push(artifactTypeKey);
  }
  @Mutation
  REMOVE_IGNORE_TYPE(artifactTypeKey: string): void {
    this.ignoreTypes = this.ignoreTypes.filter(
      (at: string) => at !== artifactTypeKey
    );
  }
  @Mutation
  SELECT_ARTIFACT(artifact: Artifact): void {
    this.selectedArtifact = artifact;
  }
  @Mutation
  UNSELECT_ARTIFACT(): void {
    this.selectedArtifact = undefined;
  }

  get getSelectedArtifact(): Artifact | undefined {
    return this.selectedArtifact;
  }
  get getSelectedSubtree(): string[] {
    return this.selectedSubtree;
  }
  get getUnselectedNodeOpacity(): number {
    return this.unselectedNodeOpacity;
  }

  get getIgnoreTypes(): string[] {
    return this.ignoreTypes;
  }
}
