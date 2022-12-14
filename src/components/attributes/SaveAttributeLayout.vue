<template>
  <div>
    <v-container v-if="isLayoutCustom">
      <v-row dense>
        <v-col cols="6">
          <v-text-field filled label="Name" v-model="editedLayout.name"
        /></v-col>
        <v-col cols="6">
          <artifact-type-input multiple v-model="editedLayout.artifactTypes"
        /></v-col>
      </v-row>
    </v-container>
    <attribute-grid editable :layout="editedLayout">
      <template v-slot:item="{ attribute }">
        <v-card outlined class="pa-2 mx-2">
          {{ attribute.label }}
        </v-card>
      </template>
    </attribute-grid>
    <flex-box v-if="isLayoutCustom" justify="space-between">
      <v-btn v-if="isUpdate" text color="error" @click="handleDelete">
        <v-icon class="mr-1">mdi-delete</v-icon>
        Delete
      </v-btn>
      <v-spacer />
      <v-btn color="primary" @click="handleSave">
        <v-icon class="mr-1">mdi-content-save</v-icon>
        Save
      </v-btn>
    </flex-box>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { AttributeLayoutSchema } from "@/types";
import { EXAMPLE_ATTRIBUTE_LAYOUTS } from "@/util";
import { AttributeGrid, ArtifactTypeInput, FlexBox } from "@/components/common";

/**
 * Allows for editing attribute layouts.
 */
export default Vue.extend({
  name: "SaveAttributeLayout",
  components: { ArtifactTypeInput, AttributeGrid, FlexBox },
  props: {
    layout: Object as PropType<AttributeLayoutSchema>,
  },
  computed: {
    /**
     * @return Whether this is a custom layout.
     */
    isLayoutCustom(): boolean {
      return this.layout?.id !== "default";
    },
    /**
     * @return The layout being edited.
     */
    editedLayout(): AttributeLayoutSchema {
      return this.layout || EXAMPLE_ATTRIBUTE_LAYOUTS[0];
    },
    /**
     * @return Whether an existing layout is being updated.
     */
    isUpdate(): boolean {
      return true;
    },
  },
  methods: {
    /**
     * Saves an attribute layout.
     */
    handleSave() {
      //TODO
    },
    /**
     * Deletes an attribute layout.
     */
    handleDelete() {
      //TODO
    },
  },
});
</script>
