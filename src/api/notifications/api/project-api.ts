import { Frame } from "webstomp-client";
import { ProjectMessage } from "@/types";
import { getProjectMembers, handleDocumentReload } from "@/api";
import { projectModule } from "@/store";

/**
 * Handles revision messages.
 *
 * @param projectId - ID of project to update.
 * @param frame - The frame of the revision.
 */
export async function projectMessageHandler(
  projectId: string,
  frame: Frame
): Promise<void> {
  const message: ProjectMessage = JSON.parse(frame.body) as ProjectMessage;
  switch (message.type) {
    case "MEMBERS":
      return getProjectMembers(projectId).then(projectModule.SET_MEMBERS);
    case "DOCUMENTS":
      return handleDocumentReload(projectId);
  }
}
