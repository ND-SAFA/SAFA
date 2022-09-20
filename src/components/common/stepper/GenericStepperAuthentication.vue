<template>
  <v-container>
    <flex-box justify="center" v-if="showWIP">
      <v-alert type="info">
        <typography
          color="white"
          value="Integrations will be enabled very soon!"
        />
      </v-alert>
    </flex-box>
    <flex-box justify="center">
      <v-btn
        large
        color="primary"
        :disabled="isDisabled"
        :loading="isLoading"
        @click="handleClick"
      >
        <v-icon class="mr-1">mdi-transit-connection-variant</v-icon>
        <span v-if="!hasCredentials">{{ disconnectedTitle }}</span>
        <span v-else>{{ connectedTitle }}</span>
      </v-btn>
    </flex-box>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { FlexBox } from "@/components/common/display";
import Typography from "@/components/common/display/Typography.vue";

/**
 * Displays an authentication stepper step.
 *
 * @emits `click` - On button click.
 */
export default Vue.extend({
  name: "GenericStepperAuthentication",
  components: { Typography, FlexBox },
  props: {
    hasCredentials: {
      type: Boolean,
      required: true,
    },
    isLoading: {
      type: Boolean,
      required: true,
    },
    disconnectedTitle: {
      type: String,
      required: true,
    },
    connectedTitle: {
      type: String,
      required: true,
    },
  },
  methods: {
    /**
     * Opens the authentication window.
     */
    handleClick(): void {
      this.$emit("click");
    },
  },
  computed: {
    showWIP(): boolean {
      return false;
    },
    /**
     * Returns whether the button is enabled.
     */
    isDisabled(): boolean {
      return this.hasCredentials || this.isLoading || this.showWIP;
    },
  },
});
</script>
