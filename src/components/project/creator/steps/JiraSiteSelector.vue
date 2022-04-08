<template>
  <v-container>
    <h1 class="text-h5">Jira Domains</h1>
    <v-divider />
    <v-progress-circular
      v-if="loading"
      indeterminate
      size="48"
      class="mx-auto my-2 d-block"
    />
    <p v-else-if="sites.length === 0" class="text-caption">
      There are no domains.
    </p>
    <v-list>
      <v-list-item-group>
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
      </v-list-item-group>
    </v-list>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { JiraCloudSite } from "@/types";

/**
 * Allows for selecting a jira domain.
 *
 * @emits `select` (JiraCloudSite) - On site selection.
 */
export default Vue.extend({
  name: "JiraSiteSelector",
  props: {
    sites: {
      type: Array as PropType<JiraCloudSite[]>,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
    },
  },
  methods: {
    handleSiteSelect(site: JiraCloudSite) {
      this.$emit("select", site);
    },
  },
});
</script>
