<template>
  <panel-card
    v-if="ENABLED_FEATURES.NASA_ARTIFACT_COMMENT"
    borderless
    collapsable
    title="Feedback"
  >
    <list-item
      v-for="comment in allComments"
      :key="comment.id"
      dense
      :class="comment.type === 'flag' ? 'bd-secondary' : 'bd-transparent'"
      style="border-width: 0 0 0 2px !important"
    >
      <flex-box>
        <icon variant="account" size="sm" />
        <div class="q-ml-md">
          <typography :value="comment.userId" />
          <typography
            secondary
            small
            :value="timestampToDisplay(comment.updatedAt)"
            l="2"
            ellipsis
          />
          <typography :value="comment.content" el="p" />
        </div>
      </flex-box>
    </list-item>
    <q-input
      v-model="newComment"
      placeholder="Add a comment..."
      class="q-ml-md bd-transparent"
      @keyup.enter="handleAddComment"
    >
      <template #before>
        <icon variant="account" size="sm" />
      </template>
      <template #append>
        <q-btn-dropdown
          flat
          auto-close
          dense
          size="sm"
          :icon="commentType === 'conversation' ? 'comment' : 'flag'"
        >
          <flex-box column>
            <text-button
              label="Comment"
              icon="comment"
              small
              block
              @click="commentType = 'conversation'"
            />
            <text-button
              label="Flag"
              icon="flag"
              small
              block
              align="start"
              @click="commentType = 'flag'"
            />
          </flex-box>
        </q-btn-dropdown>
        <icon-button
          small
          :disabled="!newComment"
          tooltip="Add comment"
          icon="forward"
          @click="handleAddComment"
        />
      </template>
    </q-input>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays artifact comments, flags, and health checks.
 */
export default {
  name: "ArtifactComments",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { ArtifactCommentsSchema, CommentSchema, CommentType } from "@/types";
import { ENABLED_FEATURES, timestampToDisplay } from "@/util";
import {
  PanelCard,
  ListItem,
  FlexBox,
  Icon,
  Typography,
  IconButton,
  TextButton,
} from "@/components/common";

const EXAMPLE_COMMENTS = ref<ArtifactCommentsSchema>({
  artifactId: "",
  comments: [
    {
      id: "1",
      content: "Hello people",
      userId: "tim@safa.ai",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      status: "active",
      type: "conversation",
    },
  ],
  flags: [
    {
      id: "2",
      content: "Oh boy there's a flag",
      userId: "tim@safa.ai",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      status: "active",
      type: "flag",
    },
  ],
  healthChecks: [],
});

const newComment = ref("");
const commentType = ref<CommentType>("conversation");

const allComments = computed(() => [
  ...EXAMPLE_COMMENTS.value.flags,
  ...EXAMPLE_COMMENTS.value.comments,
]);

function handleAddComment() {
  // TODO
  const comment: CommentSchema = {
    id: Math.random().toString(),
    content: newComment.value,
    userId: "tim@safa.ai",
    createdAt: new Date(Date.now()).toISOString(),
    updatedAt: new Date(Date.now()).toISOString(),
    status: "active",
    type: commentType.value,
  };

  if (commentType.value === "conversation") {
    EXAMPLE_COMMENTS.value.comments.push(comment);
  } else {
    EXAMPLE_COMMENTS.value.flags.push(comment);
  }

  newComment.value = "";
}
</script>
