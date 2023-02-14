<template>
  <v-tooltip bottom :disabled="tooltip.length < 20">
    <template #activator="{ props }">
      <v-list-item v-bind="props" :data-cy="dataCy" @click="handleClick">
        <v-list-item-title>
          <typography :value="item.title" data-cy="generic-list-item" />
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
import { defineComponent, PropType } from "vue";
import { ListItem } from "@/types";
import Typography from "../Typography.vue";

/**
 * Displays a generic list item.
 *
 * @emits `click` - On click.
 */
export default defineComponent({
  name: "ListItem",
  components: { Typography },
  props: {
    item: {
      type: Object as PropType<ListItem>,
      required: true,
    },
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
