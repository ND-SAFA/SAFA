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
        <icon
          :variant="comment.type === 'flag' ? 'flag' : 'account'"
          size="sm"
          class="q-mr-md"
          :color="comment.type === 'flag' ? 'secondary' : undefined"
        />
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
            <div
              v-if="comment.status !== 'resolved'"
              class="float-right show-on-hover-child"
            >
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
            <div v-else class="float-right">
              <icon-button
                small
                icon="comment"
                color="text"
                class="show-on-hover-child"
                tooltip="Mark unresolved"
                @click="handleResolveComment(comment)"
              />
              <typography secondary small value="Resolved" l="1" />
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
              text
              block
              @click="commentType = 'conversation'"
            />
            <text-button
              label="Flag"
              icon="flag"
              small
              block
              text
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
import { computed, onMounted, ref, watch } from "vue";
import { CommentSchema, CommentType } from "@/types";
import { ENABLED_FEATURES, timestampToDisplay } from "@/util";
import { commentApiStore, commentStore, selectionStore } from "@/hooks";
import {
  PanelCard,
  ListItem,
  FlexBox,
  Icon,
  Typography,
  IconButton,
  TextButton,
} from "@/components/common";

const showResolved = ref(false);
const newComment = ref("");
const commentType = ref<CommentType>("conversation");
const editedComment = ref<CommentSchema | null>(null);

const artifactId = computed(() => selectionStore.selectedArtifactId);

const allComments = computed(() =>
  commentStore.getCommentsAndFlags(artifactId.value, showResolved.value)
);

/**
 * Resets the comment input fields.
 */
function handleReset() {
  newComment.value = "";
  commentType.value = "conversation";
  editedComment.value = null;
}

/**
 * Adds a new comment to the artifact.
 */
function handleAddComment() {
  commentApiStore.handleAddComment(
    artifactId.value,
    newComment.value,
    commentType.value,
    {
      onSuccess: handleReset,
    }
  );
}

/**
 * Resolves a comment, hiding it from the list.
 * @param comment - The comment to resolve.
 */
function handleResolveComment(comment: CommentSchema) {
  commentApiStore.handleResolveComment(artifactId.value, comment);
}

/**
 * Enables a comments edit mode,
 * or disables comment editing if already enabled on the given comment.
 * @param comment - The comment to edit.
 */
function handleEditComment(comment: CommentSchema) {
  if (!editedComment.value || editedComment.value.id !== comment.id) {
    editedComment.value = comment;
  } else {
    editedComment.value = null;
  }
}

/**
 * Saves the edited comment.
 */
function handleSaveEditedComment() {
  if (!editedComment.value) return;

  commentApiStore.handleEditComment(artifactId.value, editedComment.value, {
    onSuccess: handleReset,
  });
}

/**
 * Deletes a comment.
 * @param comment - The comment to delete.
 */
function handleDeleteComment(comment: CommentSchema) {
  commentApiStore.handleDeleteComment(artifactId.value, comment.id);
}

onMounted(() => {
  commentApiStore.handleLoadComments(artifactId.value);
});

watch(
  () => artifactId.value,
  () => {
    handleReset();
    commentApiStore.handleLoadComments(artifactId.value);
  }
);
</script>
