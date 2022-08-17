import { Frame } from "webstomp-client";
import { VersionMessageModel } from "@/types";
import {
  getProjectVersion,
  handleReloadArtifacts,
  handleReloadTraceLinks,
  handleReloadWarnings,
  handleSetProject,
} from "@/api";
import { sessionModule } from "@/store";

/**
 * TODO: Delete
 * Handles revision messages related to versioned entities of the project.
 *
 * @param versionId - The project version ID of the revision.
 * @param frame - The frame received by the version websocket channel.
 */
export async function handleVersionMessage(
  versionId: string,
  frame: Frame
): Promise<void> {
  const message: VersionMessageModel = JSON.parse(frame.body);

  // Handlers for automatic entity updates.
  switch (message.type) {
    case "WARNINGS":
      return handleReloadWarnings(versionId);
  }
  // Handlers for manual entity updates.
  if (sessionModule.userEmail !== message.user) {
    switch (message.type) {
      case "VERSION":
        return getProjectVersion(versionId).then(handleSetProject);
      case "ARTIFACTS":
        return handleReloadArtifacts(versionId);
      case "TRACES":
        return handleReloadTraceLinks(versionId);
    }
  }
}
