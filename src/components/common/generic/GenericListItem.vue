<template>
  <v-tooltip bottom :disabled="tooltip.length < 20">
    <template v-slot:activator="{ on, attrs }">
      <v-list-item
        v-on="on"
        v-bind="attrs"
        :data-cy="dataCy"
        @click="handleClick"
      >
        <v-list-item-title>
          <typography :value="item.title" />
        </v-list-item-title>
        <v-list-item-subtitle v-if="!!item.subtitle">
          <typography secondary :value="item.subtitle" />
        </v-list-item-subtitle>
        <slot />
      </v-list-item>
    </template>
    <span>
      {{ tooltip }}
    </span>
  </v-tooltip>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ListItem } from "@/types";
import { Typography } from "@/components/common/display";

/**
 * Displays a generic list item.
 *
 * @emits `click` - On click.
 */
export default Vue.extend({
  name: "GenericListItem",
  components: { Typography },
  props: {
    item: Object as PropType<ListItem>,
    dataCy: String,
  },
  computed: {
    tooltip(): string {
      return this.item.subtitle
        ? `${this.item.title} - ${this.item.subtitle}`
        : this.item.title;
    },
  },
  methods: {
    /**
     * Handles button clicks by emitting them.
     */
    handleClick() {
      this.$emit("click");
    },
  },
});
</script>
