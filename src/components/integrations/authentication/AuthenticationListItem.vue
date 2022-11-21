<template>
  <v-list-item @click="handleClick">
    <v-list-item-icon>
      <v-icon v-if="!isLoading" :color="color">
        mdi-transit-connection-variant
      </v-icon>
      <v-progress-circular v-else indeterminate />
    </v-list-item-icon>
    <v-list-item-title>
      <typography variant="subtitle" :value="title" />
      <typography
        el="p"
        :value="hasCredentials ? 'Connected' : 'Not Connected'"
        :color="color"
      />
    </v-list-item-title>
    <v-list-item-action style="min-width: unset">
      <v-btn
        v-if="!hasCredentials"
        color="primary"
        outlined
        @click="handleConnect"
      >
        <v-icon class="mr-1">mdi-transit-connection-variant</v-icon>
        Connect
      </v-btn>
      <v-btn v-else color="error" outlined @click="handleDisconnect">
        <v-icon class="mr-1">mdi-delete</v-icon>
        Disconnect
      </v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script lang="ts">
import Vue from "vue";
import { Typography } from "@/components/common";

/**
 * Displays a list item & buttons for authenticating an integration.
 *
 * @emits `select` - On list item select.
 * @emits `connect` - On connect button click.
 * @emits `disconnect` - On disconnect button click.
 */
export default Vue.extend({
  name: "AuthenticationListItem",
  components: { Typography },
  props: {
    hasCredentials: {
      type: Boolean,
      required: true,
    },
    isLoading: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
  },
  computed: {
    /**
     * @return The color to render based on whether this source is connected.
     */
    color(): string {
      return this.hasCredentials ? "success" : "grey";
    },
  },
  methods: {
    /**
     * Opens the authentication window.
     */
    handleClick(): void {
      this.$emit("click");
    },
    /**
     * Opens the authentication window.
     */
    handleConnect(): void {
      this.$emit("connect");
    },
    /**
     * Disconnects the integration source
     */
    handleDisconnect(): void {
      this.$emit("disconnect");
    },
  },
});
</script>
