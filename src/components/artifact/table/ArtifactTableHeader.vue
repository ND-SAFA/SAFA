<template>
  <v-container>
    <v-row>
      <v-col>
        <v-text-field
          dense
          rounded
          outlined
          clearable
          label="Search"
          style="max-width: 600px"
          v-model="searchText"
        />
      </v-col>
      <v-col class="flex-grow-0">
        <v-row dense class="flex-nowrap">
          <v-col>
            <v-autocomplete
              outlined
              multiple
              dense
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
import { ArtifactDeltaState } from "@/types";
import { deltaTypeOptions } from "@/util";
import { deltaModule } from "@/store";
import TableColumnEditor from "./TableColumnEditor.vue";

/**
 * Represents a table of artifacts.
 *
 * @emits-1 `search` (String) - On text search.
 * @emits-1 `filter` (ArtifactDeltaState[]) - On filter search.
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
    };
  },
  computed: {
    inDeltaView(): boolean {
      return deltaModule.inDeltaView;
    },
    deltaTypes() {
      return deltaTypeOptions();
    },
  },
  watch: {
    searchText(search: string) {
      this.$emit("search", search);
    },
    selectedDeltaTypes(items: ArtifactDeltaState[]) {
      this.$emit("filter", items);
    },
  },
});
</script>

<style scoped></style>
