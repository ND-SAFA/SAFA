<template>
  <panel-card
    v-if="ENABLED_FEATURES.NASA_ARTIFACT_COMMENT"
    borderless
    collapsable
    title="Feedback"
  >
    <template #title-actions>
      <text-button
        :label="showResolved ? 'Hide Resolved' : 'Show Resolved'"
        icon="comment-resolve"
        text
        small
        @click="showResolved = !showResolved"
      />
    </template>
    <list-item
      v-for="comment in allComments"
      :key="comment.id"
      dense
      :class="comment.type === 'flag' ? 'bd-secondary' : 'bd-transparent'"
      style="border-width: 0 0 0 2px !important"
      :action-cols="3"
    >
      <flex-box full-width class="show-on-hover-parent">
        <icon variant="account" size="sm" class="q-mr-md" />
        <div class="full-width">
          <div style="height: 30px">
            <typography :value="comment.userId" />
            <typography
              secondary
              small
              :value="timestampToDisplay(comment.updatedAt)"
              l="2"
              ellipsis
            />
            <div class="float-right show-on-hover-child">
              <icon-button
                small
                icon="comment-resolve"
                color="text"
                tooltip="Resolve comment"
                @click="handleResolveComment(comment)"
              />
              <icon-button
                small
                icon="edit"
                tooltip="Edit comment"
                @click="handleEditComment(comment)"
              />
              <icon-button
                small
                icon="delete"
                tooltip="Delete comment"
                @click="handleDeleteComment(comment)"
              />
            </div>
          </div>
          <typography
            v-if="!editedComment || editedComment.id !== comment.id"
            :value="comment.content"
            el="p"
          />
          <q-input
            v-else
            v-model="editedComment.content"
            outlined
            autogrow
            type="textarea"
            dense
            class="full-width"
          >
            <template #append>
              <icon-button
                small
                icon="save"
                tooltip="Save comment"
                @click="handleSaveEditedComment"
              />
            </template>
          </q-input>
        </div>
      </flex-box>
    </list-item>
    <q-input
      v-model="newComment"
      autogrow
      type="textarea"
      placeholder="Add a comment..."
      class="q-ml-md bd-transparent"
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
      content:
        "Hello people, this is a super long comment that should wrap to multiple lines.",
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

const showResolved = ref(false);
const newComment = ref("");
const commentType = ref<CommentType>("conversation");
const editedComment = ref<CommentSchema | null>(null);

const allComments = computed(() =>
  [...EXAMPLE_COMMENTS.value.flags, ...EXAMPLE_COMMENTS.value.comments].filter(
    (comment) => showResolved.value || comment.status !== "resolved"
  )
);

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

function handleResolveComment(comment: CommentSchema) {
  // TODO
  comment.status = "resolved";
}

function handleEditComment(comment: CommentSchema) {
  // TODO
  if (!editedComment.value || editedComment.value.id !== comment.id) {
    editedComment.value = comment;
  } else {
    editedComment.value = null;
  }
}

function handleSaveEditedComment() {
  // TODO
  if (!editedComment.value) return;

  editedComment.value = null;
}

function handleDeleteComment(comment: CommentSchema) {
  // TODO
  EXAMPLE_COMMENTS.value.comments = EXAMPLE_COMMENTS.value.comments.filter(
    (c) => c.id !== comment.id
  );
  EXAMPLE_COMMENTS.value.flags = EXAMPLE_COMMENTS.value.flags.filter(
    (c) => c.id !== comment.id
  );
}
</script>
