import { Frame } from "webstomp-client";
import { ProjectMessageModel } from "@/types";
import { getProjectMembers, handleDocumentReload } from "@/api";
import { projectModule } from "@/store";

/**
 * TODO: Delete
 * Handles revision messages.
 *
 * @param projectId - ID of project to update.
 * @param frame - The frame of the revision.
 */
export async function handleProjectMessage(
  projectId: string,
  frame: Frame
): Promise<void> {
  const message: ProjectMessageModel = JSON.parse(frame.body);
  switch (message.type) {
    case "MEMBERS":
      return getProjectMembers(projectId).then(projectModule.SET_MEMBERS);
    case "DOCUMENTS":
      return handleDocumentReload(projectId);
  }
}
