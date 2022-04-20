<template>
  <div>
    <div v-for="{ id, name, dataType, required } in columns" :key="id">
      <v-text-field
        filled
        v-if="isFreeText(dataType)"
        :label="name"
        :hint="required ? 'Requires a non-empty value' : ''"
        :value="getStringModel(id)"
        @input="setStringModel(id, $event)"
      />
      <v-combobox
        filled
        multiple
        chips
        deletable-chips
        v-if="isSelect(dataType)"
        :label="name"
        :hint="required ? 'Requires a non-empty value' : ''"
        :value="getArrayModel(id)"
        @input="setArrayModel(id, $event)"
      />
      <artifact-input
        only-document-artifacts
        v-if="isRelation(dataType)"
        :label="name"
        :hint="required ? 'Requires a non-empty value' : ''"
        :value="getArrayModel(id)"
        @input="setArrayModel(id, $event)"
      />
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Artifact, ColumnDataType, DocumentColumn } from "@/types";
import { documentModule } from "@/store";
import ArtifactInput from "./ArtifactInput.vue";

/**
 * An input for any custom fields defined in the current document.
 */
export default Vue.extend({
  name: "CustomFieldInput",
  components: { ArtifactInput },
  props: {
    value: {
      type: Object as PropType<Artifact>,
      required: true,
    },
  },
  data() {
    return {
      model: this.value,
      showPassword: false,
    };
  },
  computed: {
    /**
     * @return The current document columns.
     */
    columns(): DocumentColumn[] {
      return documentModule.tableColumns;
    },
  },
  methods: {
    /**
     * Returns the string value of a field.
     * @param columnId - The field to find.
     * @return The column value.
     */
    getStringModel(columnId: string): string {
      return this.value.customFields?.[columnId] || "";
    },
    /**
     * Sets the string value of a field.
     * @param columnId - The field to find.
     * @param value - The value to set.
     */
    setStringModel(columnId: string, value: string) {
      if (!this.value.customFields) {
        this.value.customFields = {};
      }
      this.value.customFields[columnId] = value;
    },

    /**
     * Returns the array value of a field.
     * @param columnId - The field to find.
     * @return The column array value.
     */
    getArrayModel(columnId: string): string[] {
      const value = this.value.customFields?.[columnId];
      return value ? value.split("||") : [];
    },
    /**
     * Sets the string value of an array field.
     * @param columnId - The field to find.
     * @param value - The value to set.
     */
    setArrayModel(columnId: string, value: string[]) {
      if (!this.value.customFields) {
        this.value.customFields = {};
      }
      this.value.customFields[columnId] = value.join("||");
    },

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
  },
});
</script>
