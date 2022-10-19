import {
  clearSubscriptions,
  connect,
  Endpoint,
  fillEndpoint,
  stompClient,
} from "@/api";
import { handleEntityChangeMessage } from "./message-handler";

/**
 * Connects and subscribes to the given project and version.
 *
 * @param projectId - The project ID to connect to.
 * @param versionId - The project version ID to connect to.
 */
export async function handleSelectVersion(
  projectId: string,
  versionId: string
): Promise<void> {
  if (!projectId || !versionId) {
    return;
  }

  await connect();

  clearSubscriptions();

  stompClient.subscribe(
    fillEndpoint(Endpoint.projectTopic, { projectId }),
    (frame) => handleEntityChangeMessage(versionId, frame)
  );

  stompClient.subscribe(
    fillEndpoint(Endpoint.versionTopic, { versionId }),
    (frame) => handleEntityChangeMessage(versionId, frame)
  );
}
