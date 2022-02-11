<template>
  <v-autocomplete
    filled
    chips
    multiple
    deletable-chips
    label="Visible Artifacts"
    v-model="model"
    :items="artifacts"
    item-text="name"
    item-value="id"
    :filter="filter"
    @keydown.enter="$emit('enter')"
  >
    <template v-slot:item="{ item }">
      <v-list-item-content style="max-width: 300px">
        <v-list-item-title
          v-html="`${getTypePrintName(item.type)} - ${item.name}`"
        />
        <v-list-item-subtitle v-if="!isExpanded(item)" v-html="item.body" />
        <v-list-item-content v-if="isExpanded(item)" v-html="item.body" />
        <v-list-item-action class="ma-0">
          <v-spacer />
          <v-btn text small @click.stop="handleSeeMore(item)">
            {{ isExpanded(item) ? "See Less" : "See More" }}
          </v-btn>
        </v-list-item-action>
      </v-list-item-content>
    </template>
  </v-autocomplete>
</template>

<script lang="ts">
import Vue from "vue";
import { Artifact } from "@/types";
import { artifactModule } from "@/store";
import { getArtifactTypePrintName } from "@/util";

/**
 * An input for artifacts.
 *
 * @emits `input` (Artifact[]) - On input change.
 * @emits `enter` - On submit.
 */
export default Vue.extend({
  name: "artifact-input",
  props: {
    value: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      model: this.value,
      showPassword: false,
      expandedId: "",
    };
  },
  methods: {
    getTypePrintName: getArtifactTypePrintName,
    filter(item: Artifact, queryText: string): boolean {
      const lowercaseQuery = queryText.toLowerCase();

      return (
        item.name.toLowerCase().includes(lowercaseQuery) ||
        item.type.toLowerCase().includes(lowercaseQuery) ||
        this.getTypePrintName(item.type).toLowerCase().includes(lowercaseQuery)
      );
    },
    handleSeeMore(item: Artifact) {
      this.expandedId = item.id === this.expandedId ? "" : item.id;
    },
    isExpanded(item: Artifact): boolean {
      return item.id === this.expandedId;
    },
  },
  computed: {
    artifacts(): Artifact[] {
      return artifactModule.allArtifacts;
    },
  },
  watch: {
    value(currentValue: string[]) {
      this.model = currentValue;
    },
    model(currentValue: string[]) {
      this.$emit("input", currentValue);
    },
  },
});
</script>
