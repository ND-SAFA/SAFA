<template>
  <v-container>
    <v-row>
      <slot name="panels" />
    </v-row>
    <v-row align="center" class="mx-auto width-fit">
      <v-col>
        <v-btn
          color="primary"
          :disabled="isButtonDisabled"
          @click="$emit('add')"
        >
          Create new {{ itemName }}
        </v-btn>
      </v-col>
      <v-col v-if="showError">
        <typography :value="`Requires at least 1 ${itemName}.`" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ThemeColors } from "@/util";
import { Typography } from "@/components/common";

/**
 * Validated upload panels.
 *
 * @emits-1 `upload:valid` - On upload is valid.
 * @emits-2 `upload:invalid` - On upload is invalid.
 * @emits-3 `add` - On add.
 */
export default Vue.extend({
  name: "ValidatedPanels",
  components: { Typography },
  props: {
    itemName: {
      type: String,
      required: true,
    },
    isValidStates: {
      type: Array as PropType<boolean[]>,
      required: true,
    },
    showError: {
      type: Boolean,
      required: true,
    },
    defaultValidState: {
      type: Boolean,
      required: true,
    },
    isButtonDisabled: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      errorColor: ThemeColors.error,
    };
  },
  computed: {
    /**
     * @return Whether the panel is valid.
     */
    isValid(): boolean {
      if (this.isValidStates.length === 0) return this.defaultValidState;
      return this.isValidStates.filter((isValid) => !isValid).length === 0;
    },
  },
  watch: {
    /**
     * Emits changes when a panel changes is validated status.
     */
    isValid(isValid: boolean): void {
      if (isValid) {
        this.$emit("upload:valid");
      } else {
        this.$emit("upload:invalid");
      }
    },
  },
});
</script>
