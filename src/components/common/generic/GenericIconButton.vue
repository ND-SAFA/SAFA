<template>
  <v-tooltip bottom z-index="10000">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        v-on="on"
        v-bind="attrs"
        :color="color"
        :icon="!fab"
        :fab="fab"
        :class="disabled ? 'disable-events' : ''"
        :small="small"
        :large="large"
        :hidden="isHidden"
        :data-cy="dataCy"
        @click="$emit('click')"
      >
        <v-icon :style="iconStyle">{{ iconId }}</v-icon>
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
    dataCy: String,
    tooltip: {
      type: String,
      required: true,
    },
    iconId: {
      type: String,
      required: true,
    },
    color: String,
    iconStyle: String,
    fab: Boolean,
    small: Boolean,
    large: Boolean,
    isDisabled: Boolean,
    isHidden: Boolean,
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
