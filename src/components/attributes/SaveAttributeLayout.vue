<template>
  <div>
    <flex-box v-if="store.isCustom" justify="space-between" b="4">
      <v-btn v-if="store.isUpdate" text color="error" @click="handleDelete">
        <v-icon class="mr-1">mdi-delete</v-icon>
        Delete
      </v-btn>
      <v-spacer />
      <v-btn :disabled="!store.canSave" color="primary" @click="handleSave">
        <v-icon class="mr-1">mdi-content-save</v-icon>
        Save
      </v-btn>
    </flex-box>
    <v-row dense v-if="store.isCustom">
      <v-col cols="6">
        <v-text-field filled label="Name" v-model="store.editedLayout.name"
      /></v-col>
      <v-col cols="6">
        <artifact-type-input
          multiple
          v-model="store.editedLayout.artifactTypes"
      /></v-col>
    </v-row>
    <panel-card>
      <attribute-grid editable :layout="store.editedLayout">
        <template v-slot:item="{ attribute }">
          <v-card outlined class="pa-2 mx-2">
            {{ attribute.label }}
          </v-card>
        </template>
      </attribute-grid>
    </panel-card>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { AttributeLayoutSchema } from "@/types";
import { attributeLayoutSaveStore } from "@/hooks";
import {
  AttributeGrid,
  ArtifactTypeInput,
  FlexBox,
  PanelCard,
} from "@/components/common";

/**
 * Allows for editing attribute layouts.
 */
export default Vue.extend({
  name: "SaveAttributeLayout",
  components: { PanelCard, ArtifactTypeInput, AttributeGrid, FlexBox },
  props: {
    layout: Object as PropType<AttributeLayoutSchema>,
  },
  data() {
    return {
      store: attributeLayoutSaveStore(this.layout?.id || ""),
    };
  },
  mounted() {
    this.store.resetLayout(this.layout);
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
