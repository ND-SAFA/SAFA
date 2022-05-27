import { Frame } from "webstomp-client";
import { VersionMessage } from "@/types";
import {
  getProjectVersion,
  handleReloadArtifacts,
  handleReloadTraceLinks,
  handleReloadWarnings,
  handleSetProject,
} from "@/api";
import { sessionModule } from "@/store";

/**
 * Handles revision messages related to versioned entities of the project.
 *
 * @param versionId - The project version ID of the revision.
 * @param frame - The frame received by the version websocket channel.
 */
export async function versionApi(
  versionId: string,
  frame: Frame
): Promise<void> {
  const message: VersionMessage = JSON.parse(frame.body) as VersionMessage;

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
