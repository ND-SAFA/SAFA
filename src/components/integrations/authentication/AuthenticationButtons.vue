<template>
  <flex-box justify="center" align="center" b="2">
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
    <v-btn
      v-if="hasCredentials"
      large
      color="error"
      outlined
      class="ml-2"
      @click="$emit('delete')"
    >
      <v-icon class="mr-1">mdi-delete</v-icon>
      Disconnect
    </v-btn>
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import { FlexBox } from "@/components/common/display";

/**
 * Displays buttons for authenticating an integration.
 *
 * @emits `click` - On button click.
 * @emits `delete` - On disconnect
 */
export default Vue.extend({
  name: "AuthenticationButtons",
  components: { FlexBox },
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
    /**
     * Returns whether the button is enabled.
     */
    isDisabled(): boolean {
      return this.hasCredentials || this.isLoading;
    },
  },
});
</script>
