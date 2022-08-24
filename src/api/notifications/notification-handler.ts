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

  /**
   * Project and Version topics are transmit {@link EntityChangeMessage}.
   * The difference is that the project topic transmits non-version specific
   * data (e.g. artifact types) while the version topic does.
   */
  stompClient.subscribe(
    fillEndpoint(Endpoint.projectTopic, { projectId }),
    (frame) => handleEntityChangeMessage(versionId, frame)
  );

  stompClient.subscribe(
    fillEndpoint(Endpoint.versionTopic, { versionId }),
    (frame) => handleEntityChangeMessage(versionId, frame)
  );
}
