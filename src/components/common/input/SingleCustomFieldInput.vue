<template>
  <div>
    <v-text-field
      :filled="filled"
      v-if="isFreeText()"
      :label="column.name"
      :hint="column.required ? 'Requires a non-empty value' : ''"
      :value="getStringModel()"
      @input="setStringModel($event)"
    />
    <v-combobox
      :filled="filled"
      multiple
      chips
      deletable-chips
      v-if="isSelect()"
      :label="column.name"
      :hint="column.required ? 'Requires a non-empty value' : ''"
      :value="getArrayModel()"
      @input="setArrayModel($event)"
    />
    <artifact-input
      :filled="filled"
      only-document-artifacts
      v-if="isRelation()"
      :label="column.name"
      :hint="column.required ? 'Requires a non-empty value' : ''"
      :value="getArrayModel()"
      @input="setArrayModel($event)"
    />
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactModel, ColumnDataType, ColumnModel } from "@/types";
import ArtifactInput from "./ArtifactInput.vue";

/**
 * An input for a custom field defined in the current document.
 *
 * @emits-1 `change:custom` - Called when a custom field is changed.
 */
export default Vue.extend({
  name: "SingleCustomFieldInput",
  components: { ArtifactInput },
  props: {
    value: {
      type: Object as PropType<ArtifactModel>,
      required: true,
    },
    column: {
      type: Object as PropType<ColumnModel>,
      required: true,
    },
    filled: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      model: this.value,
      showPassword: false,
    };
  },
  methods: {
    /**
     * Returns the string value of a field.
     * @return The column value.
     */
    getStringModel(): string {
      return this.value.customFields?.[this.column.id] || "";
    },
    /**
     * Sets the string value of a field.
     * @param value - The value to set.
     */
    setStringModel(value: string) {
      if (!this.value.customFields) {
        this.value.customFields = {};
      }
      this.value.customFields[this.column.id] = value;
      this.$emit("change:custom");
    },

    /**
     * Returns the array value of a field.
     * @return The column array value.
     */
    getArrayModel(): string[] {
      const value = this.value.customFields?.[this.column.id];
      return value ? value.split("||") : [];
    },
    /**
     * Sets the string value of an array field.
     * @param value - The value to set.
     */
    setArrayModel(value: string[]) {
      if (!this.value.customFields) {
        this.value.customFields = {};
      }
      this.value.customFields[this.column.id] = value.join("||");
      this.$emit("change:custom");
    },

    /**
     * @return Whether the data type is free text.
     */
    isFreeText(): boolean {
      return this.column.dataType === ColumnDataType.FREE_TEXT;
    },
    /**
     * @return Whether the data type is a relation.
     */
    isRelation(): boolean {
      return this.column.dataType === ColumnDataType.RELATION;
    },
    /**
     * @return Whether the data type is a select.
     */
    isSelect(): boolean {
      return this.column.dataType === ColumnDataType.SELECT;
    },
  },
});
</script>
