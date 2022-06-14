<template>
  <div
    class="d-flex flex-row align-center justify-space-between"
    style="height: 100%"
    v-if="!isEditMode"
    @mouseover="showEditButton = true"
    @mouseout="showEditButton = false"
  >
    <v-icon
      v-if="column.required && !item[column.id]"
      :key="artifact.id"
      :color="errorColor"
    >
      mdi-information-outline
    </v-icon>
    <div v-if="isFreeText(column.dataType)">
      <span class="text-body-1">{{ item[column.id] || "" }}</span>
    </div>
    <div v-if="isRelation(column.dataType)">
      <artifact-table-chip
        v-for="artifactId in getArrayValue(item[column.id])"
        :key="artifactId"
        :text="getArtifactName(artifactId)"
      />
    </div>
    <div v-if="isSelect(column.dataType)">
      <artifact-table-chip
        v-for="val in getArrayValue(item[column.id])"
        :key="val"
        :text="val"
      />
    </div>
    <generic-icon-button
      class="ml-1"
      icon-id="mdi-pencil"
      :tooltip="`Edit '${column.name}'`"
      :is-hidden="!showEditButton"
      @click="isEditMode = true"
    />
  </div>
  <div v-else class="d-flex flex-row align-center">
    <single-custom-field-input
      :column="column"
      :value="artifact"
      :filled="false"
    />
    <generic-icon-button
      class="ml-1"
      icon-id="mdi-content-save"
      :tooltip="`Save '${column.name}'`"
      @click="handleSaveEdit"
    />
    <generic-icon-button
      class="ml-1"
      icon-id="mdi-close-circle"
      :tooltip="`Cancel editing '${column.name}'`"
      @click="handleCancelEdit"
    />
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  Artifact,
  ColumnDataType,
  DocumentColumn,
  FlatArtifact,
} from "@/types";
import ArtifactTableChip from "./ArtifactTableChip.vue";
import { artifactModule } from "@/store";
import { ThemeColors } from "@/util";
import { GenericIconButton, SingleCustomFieldInput } from "@/components/common";
import { handleSaveArtifact } from "@/api";

/**
 * Displays a cell in the artifact table.
 */
export default Vue.extend({
  name: "ArtifactTableCell",
  components: {
    GenericIconButton,
    ArtifactTableChip,
    SingleCustomFieldInput,
  },
  props: {
    item: {
      type: Object as PropType<FlatArtifact>,
      required: true,
    },
    column: {
      type: Object as PropType<DocumentColumn>,
      required: true,
    },
  },
  data() {
    return {
      errorColor: ThemeColors.error,
      showEditButton: false,
      isEditMode: false,
      baseValue: this.item[this.column.id],
    };
  },
  computed: {
    /**
     * Returns the associated artifact for this cell.
     */
    artifact(): Artifact {
      return artifactModule.getArtifactById(this.item.id);
    },
  },
  methods: {
    /**
     * @param dataType - The data type to check.
     * @return Whether the data type is free text.
     */
    isFreeText(dataType: ColumnDataType): boolean {
      return dataType === ColumnDataType.FREE_TEXT;
    },
    /**
     * @param dataType - The data type to check.
     * @return Whether the data type is a relation.
     */
    isRelation(dataType: ColumnDataType): boolean {
      return dataType === ColumnDataType.RELATION;
    },
    /**
     * @param dataType - The data type to check.
     * @return Whether the data type is a select.
     */
    isSelect(dataType: ColumnDataType): boolean {
      return dataType === ColumnDataType.SELECT;
    },
    /**
     * Returns the artifact name of the given artifact id.
     * @param id - The artifact to find.
     * @return The artifact name.
     */
    getArtifactName(id: string): string {
      return artifactModule.getArtifactById(id).name;
    },
    /**
     * Returns the value of an array custom field.
     * @param itemValue - The stored array value.
     * @return The stored value as an array.
     */
    getArrayValue(itemValue?: string): string[] {
      return itemValue?.split("||") || [];
    },
    /**
     * Resets the value of a cell.
     */
    resetCellValue() {
      const artifact = this.artifact;

      if (!artifact.customFields) return;

      artifact.customFields[this.column.id] = this.baseValue;
    },
    /**
     * Saves changes to this cell.
     */
    handleSaveEdit() {
      handleSaveArtifact(this.artifact, true, undefined, {
        onSuccess: () => (this.isEditMode = false),
        onError: () => {
          this.isEditMode = false;
          this.resetCellValue();
        },
      });
    },
    /**
     * Cancels changes to this cell.
     */
    handleCancelEdit() {
      this.isEditMode = false;
      this.resetCellValue();
    },
  },
});
</script>
