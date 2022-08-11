<template>
  <v-container>
    <v-row align="center">
      <v-col>
        <v-text-field
          dense
          outlined
          clearable
          hide-details
          label="Search Artifacts"
          style="max-width: 600px"
          v-model="searchText"
          append-icon="mdi-magnify"
        />
      </v-col>
      <v-col class="flex-grow-0">
        <v-row dense class="flex-nowrap">
          <v-col>
            <v-autocomplete
              outlined
              multiple
              dense
              hide-details
              v-if="inDeltaView"
              label="Delta Types"
              v-model="selectedDeltaTypes"
              :items="deltaTypes"
              item-text="name"
              item-value="id"
              style="width: 200px"
            />
          </v-col>
          <v-col>
            <table-column-editor />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactDeltaState, DocumentType } from "@/types";
import { deltaTypeOptions } from "@/util";
import { appModule, deltaModule } from "@/store";
import TableColumnEditor from "./TableColumnEditor.vue";

/**
 * Represents the header and inputs for a table of artifacts.
 *
 * @emits-1 `search` (String) - On text search.
 * @emits-2 `filter` (ArtifactDeltaState[]) - On filter search.
 */
export default Vue.extend({
  name: "ArtifactTableHeader",
  components: {
    TableColumnEditor,
  },
  data() {
    return {
      searchText: "",
      selectedDeltaTypes: [] as ArtifactDeltaState[],
      deltaTypes: deltaTypeOptions(),
    };
  },
  computed: {
    /**
     * @return Whether the app is in delta view.
     */
    inDeltaView(): boolean {
      return deltaModule.inDeltaView;
    },
  },
  watch: {
    /**
     * Emits the current search text on change.
     */
    searchText(search: string) {
      this.$emit("search", search);
    },
    /**
     * Emits the selected delta types on change.
     */
    selectedDeltaTypes(items: ArtifactDeltaState[]) {
      this.$emit("filter", items);
    },
  },
  methods: {
    /**
     * Opens the create artifact window.
     */
    handleCreate() {
      appModule.openArtifactCreatorTo({
        isNewArtifact: true,
        type: DocumentType.FMEA,
      });
    },
  },
});
</script>

<style scoped></style>
