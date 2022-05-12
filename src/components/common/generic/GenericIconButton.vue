<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        v-on="on"
        v-bind="attrs"
        :color="color"
        :icon="!fab"
        :fab="fab"
        :class="disabled ? 'disable-events' : ''"
        :small="small"
        @click="$emit('click')"
      >
        <v-icon>{{ iconId }}</v-icon>
      </v-btn>
    </template>
    <span>{{ tooltip }}</span>
  </v-tooltip>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * A generic icon button.
 *
 * @emits `click` - On button click.
 */
export default Vue.extend({
  name: "GenericIconButton",
  props: {
    tooltip: {
      type: String,
      required: true,
    },
    iconId: {
      type: String,
      required: true,
    },
    color: String,
    fab: Boolean,
    small: Boolean,
    isDisabled: Boolean,
  },
  computed: {
    /**
     * @return Whether the button is disabled.
     */
    disabled(): boolean {
      return this.isDisabled === undefined ? false : this.isDisabled;
    },
  },
});
</script>
