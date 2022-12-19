<template>
  <v-btn
    :outlined="outlined"
    :text="text"
    :disabled="disabled"
    :large="large"
    :block="block"
    :loading="loading"
    :color="buttonColor"
    :value="value"
    :class="buttonClassName"
    :data-cy="dataCy"
    @click="$emit('click')"
  >
    <v-icon v-if="buttonIconId" class="mr-1">{{ buttonIconId }}</v-icon>
    <slot />
  </v-btn>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

/**
 * A generic text button.
 *
 * @emits-1 `click` - On click.
 */
export default Vue.extend({
  name: "TextButton",
  props: {
    outlined: Boolean,
    text: Boolean,
    disabled: Boolean,
    large: Boolean,
    block: Boolean,
    loading: Boolean,
    color: String,
    iconId: String,
    value: String,
    y: String,
    x: String,
    classes: String,
    variant: String as PropType<
      "add" | "edit" | "save" | "delete" | "cancel" | "artifact"
    >,
    dataCy: String,
  },
  computed: {
    /**
     * @return The icon to render.
     */
    buttonIconId(): string | undefined {
      switch (this.variant) {
        case "add":
          return "mdi-plus";
        case "edit":
          return "mdi-pencil";
        case "save":
          return "mdi-content-save";
        case "delete":
          return "mdi-delete";
        case "cancel":
          return "mdi-close";
        case "artifact":
          return "mdi-application-array-outline";
        default:
          return this.iconId;
      }
    },
    /**
     * @return The color to render.
     */
    buttonColor(): string | undefined {
      switch (this.variant) {
        case "add":
        case "save":
          return "primary";
        case "delete":
          return "error";
        default:
          return this.color;
      }
    },
    /**
     * @return The button's class name.
     */
    buttonClassName(): string {
      let classNames = this.classes || "";

      if (this.x) classNames += ` mx-${this.x}`;
      if (this.y) classNames += ` my-${this.y}`;

      return classNames;
    },
  },
});
</script>
