<template>
  <v-container v-if="isTableView">
    <v-data-table
      class="elevation-1"
      :headers="headers"
      :items="items"
      :search="searchText"
      :item-class="getItemBackground"
    >
      <template v-slot:top>
        <artifact-table-header
          @search="searchText = $event"
          @filter="selectedDeltaTypes = $event"
        />
      </template>
      <template
        v-for="{ id, dataType, required } in columns"
        v-slot:[`item.${id}`]="{ item }"
      >
        <v-divider
          v-if="required && !item[id]"
          :key="id"
          :style="`border-color: ${errorColor}; width: 40px`"
        />
        <span v-if="isFreeText(dataType)" class="text-body-1" :key="id">
          {{ item[id] || "" }}
        </span>
        <div v-if="isRelation(dataType)" :key="id">
          <artifact-table-chip
            v-for="artifactId in getArrayValue(item[id])"
            :key="artifactId"
            :text="getArtifactName(artifactId)"
          />
        </div>
        <div v-if="isSelect(dataType)" :key="id">
          <artifact-table-chip
            v-for="val in getArrayValue(item[id])"
            :key="val"
            :text="val"
          />
        </div>
      </template>
      <template v-slot:item.actions="{ item }">
        <generic-icon-button
          icon-id="mdi-pencil"
          tooltip="Edit"
          @click="handleEdit(item)"
        />
        <generic-icon-button
          icon-id="mdi-delete"
          tooltip="Delete"
          @click="handleDelete(item)"
        />
      </template>
      <template v-slot:footer>
        <v-row justify="end" class="mr-2 mt-1">
          <generic-icon-button
            fab
            color="primary"
            icon-id="mdi-plus"
            tooltip="Create"
            @click="handleCreate"
          />
        </v-row>

        <artifact-creator-modal
          :title="artifactCreatorTitle"
          :is-open="createDialogueOpen"
          :artifact="selectedArtifact"
          @close="handleCloseModal"
        />
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import {
  Artifact,
  ArtifactDeltaState,
  ColumnDataType,
  DocumentType,
} from "@/types";
import { ThemeColors } from "@/util";
import { artifactModule, deltaModule, documentModule } from "@/store";
import { deleteArtifactFromCurrentVersion } from "@/api";
import { ArtifactCreatorModal, GenericIconButton } from "@/components/common";
import ArtifactTableChip from "./ArtifactTableChip.vue";
import ArtifactTableHeader from "./ArtifactTableHeader.vue";

type FlatArtifact = Artifact & Record<string, string>;

/**
 * Represents a table of artifacts.
 */
export default Vue.extend({
  name: "ArtifactTable",
  components: {
    ArtifactTableHeader,
    ArtifactTableChip,
    GenericIconButton,
    ArtifactCreatorModal,
  },
  data() {
    return {
      selectedArtifact: undefined as Artifact | undefined,
      createDialogueOpen: false as boolean | DocumentType.FMEA,
      searchText: "",
      selectedDeltaTypes: [] as ArtifactDeltaState[],
    };
  },
  computed: {
    inDeltaView(): boolean {
      return deltaModule.inDeltaView;
    },
    isTableView(): boolean {
      return documentModule.isTableDocument;
    },

    headers() {
      return [
        {
          text: "Name",
          value: "name",
        },
        ...documentModule.tableColumns.map((col) => ({
          text: col.name,
          value: col.id,
        })),
        {
          text: "Actions",
          value: "actions",
          width: "120px",
        },
      ];
    },
    columns() {
      return documentModule.tableColumns;
    },
    items(): FlatArtifact[] {
      return artifactModule.artifacts
        .filter(
          (item) =>
            !this.inDeltaView ||
            this.selectedDeltaTypes.length === 0 ||
            this.selectedDeltaTypes.includes(
              deltaModule.getArtifactDeltaType(item.id)
            )
        )
        .map(
          (artifact) =>
            ({
              ...artifact,
              ...artifact.customFields,
            } as FlatArtifact)
        );
    },

    artifactCreatorTitle(): string {
      return this.selectedArtifact ? "Edit Artifact" : "Create Artifact";
    },
    errorColor(): string {
      return ThemeColors.error;
    },
  },
  methods: {
    handleEdit(artifact: Artifact) {
      this.selectedArtifact = artifact;
      this.createDialogueOpen = true;
    },
    handleDelete(artifact: Artifact) {
      deleteArtifactFromCurrentVersion(artifact);
    },
    handleCreate() {
      this.createDialogueOpen = DocumentType.FMEA;
    },
    handleCloseModal() {
      this.createDialogueOpen = false;
      this.selectedArtifact = undefined;
    },

    isFreeText(dataType: ColumnDataType): boolean {
      return dataType === ColumnDataType.FREE_TEXT;
    },
    isRelation(dataType: ColumnDataType): boolean {
      return dataType === ColumnDataType.RELATION;
    },
    isSelect(dataType: ColumnDataType): boolean {
      return dataType === ColumnDataType.SELECT;
    },

    getArtifactName(id: string): string {
      return artifactModule.getArtifactById(id).name;
    },
    getArrayValue(itemValue?: string): string[] {
      return itemValue?.split("||") || [];
    },

    getItemBackground(item: Artifact): string {
      const deltaState = deltaModule.getArtifactDeltaType(item.id);

      switch (deltaState) {
        case ArtifactDeltaState.ADDED:
          return "artifact-added";
        case ArtifactDeltaState.MODIFIED:
          return "artifact-modified";
        case ArtifactDeltaState.REMOVED:
          return "artifact-removed";
        default:
          return "";
      }
    },
  },
});
</script>
