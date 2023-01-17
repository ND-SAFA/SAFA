<template>
  <v-list-item :inactive="inactive || !hasCredentials" @click="handleClick">
    <v-list-item-icon style="align-self: center">
      <v-icon v-if="!isLoading" :color="color">
        mdi-transit-connection-variant
      </v-icon>
      <v-progress-circular v-else indeterminate />
    </v-list-item-icon>
    <v-list-item-title>
      <typography variant="subtitle" :value="title" />
      <typography
        el="div"
        :value="hasCredentials ? 'Connected' : 'Not Connected'"
        :color="color"
      />
    </v-list-item-title>
    <v-list-item-action style="min-width: unset">
      <text-button
        v-if="!hasCredentials"
        color="primary"
        outlined
        icon-id="mdi-transit-connection-variant"
        @click="handleConnect"
      >
        Connect
      </text-button>
      <flex-box v-else column align="end">
        <text-button
          outlined
          variant="add"
          classes="mb-2"
          @click="handleConnect"
        >
          Installation
        </text-button>
        <text-button outlined variant="delete" @click="handleDisconnect">
          Disconnect
        </text-button>
      </flex-box>
    </v-list-item-action>
  </v-list-item>
</template>

<script lang="ts">
import Vue from "vue";
import { Typography, TextButton } from "@/components/common";
import FlexBox from "@/components/common/layout/FlexBox.vue";

/**
 * Displays a list item & buttons for authenticating an integration.
 *
 * @emits `select` - On list item select.
 * @emits `connect` - On connect button click.
 * @emits `disconnect` - On disconnect button click.
 */
export default Vue.extend({
  name: "AuthenticationListItem",
  components: { FlexBox, TextButton, Typography },
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
    inactive: Boolean,
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
