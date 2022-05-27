import {
  clearSubscriptions,
  connect,
  Endpoint,
  fillEndpoint,
  projectMessageHandler,
  stompClient,
  versionApi,
} from "@/api";

/**
 * Connects and subscribes to the given project and version.
 *
 * @param projectId - The project ID to connect to.
 * @param versionId - The project version ID to connect to.
 */
export function handlers(projectId: string, versionId: string): Promise<void> {
  return new Promise((resolve, reject) => {
    if (!projectId || !versionId) {
      resolve();
      return;
    }

    connect()
      .then(() => {
        clearSubscriptions();
        stompClient.subscribe(
          fillEndpoint(Endpoint.submitJobProject, { projectId }),
          async (frame) => {
            await projectMessageHandler(projectId, frame);
          }
        );
        stompClient.subscribe(
          fillEndpoint(Endpoint.submitJobVersion, { projectId }),
          async (frame) => {
            await versionApi(versionId, frame);
          }
        );
        resolve();
      })
      .catch(reject);
  });
}
