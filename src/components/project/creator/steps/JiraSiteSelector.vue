<template>
  <generic-stepper-list-step
    empty-message="There are no domains."
    :item-count="sites.length"
    :loading="loading"
    title="Jira Domains"
  >
    <template slot="items">
      <template v-for="site in sites">
        <v-list-item :key="site.id" @click="handleSiteSelect(site)">
          <v-list-item-icon>
            <v-avatar>
              <img :src="site.avatarUrl" :alt="site.name" />
            </v-avatar>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="site.name" />

            <v-list-item-subtitle v-text="site.url" />
          </v-list-item-content>
        </v-list-item>
      </template>
    </template>
  </generic-stepper-list-step>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { JiraCloudSiteModel } from "@/types";
import { GenericStepperListStep } from "@/components";

/**
 * Allows for selecting a jira domain.
 *
 * @emits `select` (JiraCloudSite) - On site selection.
 */
export default Vue.extend({
  name: "JiraSiteSelector",
  components: {
    GenericStepperListStep,
  },
  props: {
    sites: {
      type: Array as PropType<JiraCloudSiteModel[]>,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
    },
  },
  methods: {
    /**
     * Handles a click to select a site.
     * @param site - The site to select.
     */
    handleSiteSelect(site: JiraCloudSiteModel) {
      this.$emit("select", site);
    },
  },
});
</script>
