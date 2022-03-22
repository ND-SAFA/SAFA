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
import ArtifactInput from "@/components/common/input/ArtifactInput.vue";

/**
 * An input for any custom fields defined in the current document.
 */
export default Vue.extend({
  name: "custom-field-input",
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
    columns(): DocumentColumn[] {
      return documentModule.tableColumns;
    },
  },
  methods: {
    getStringModel(columnId: string): string {
      return this.value.customFields?.[columnId] || "";
    },
    setStringModel(columnId: string, value: string) {
      if (!this.value.customFields) {
        this.value.customFields = {};
      }
      this.value.customFields[columnId] = value;
    },
    getArrayModel(columnId: string): string[] {
      const value = this.value.customFields?.[columnId];
      return value ? value.split("||") : [];
    },
    setArrayModel(columnId: string, value: string[]) {
      if (!this.value.customFields) {
        this.value.customFields = {};
      }
      this.value.customFields[columnId] = value.join("||");
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
  },
});
</script>
