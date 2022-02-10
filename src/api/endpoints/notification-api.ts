import SockJS from "sockjs-client";
import Stomp, { Client, Frame } from "webstomp-client";
import { ProjectMessage, VersionMessage } from "@/types";
import { projectModule, logModule } from "@/store";
import { baseURL } from "@/api/util";
import { getProjectVersion } from "@/api/endpoints/version-api";
import { setCreatedProject } from "@/api/handlers/set-project-handler";
import { getProjectMembers } from "@/api";
import { getProjectDocuments } from "@/api/endpoints/document-api";

const WEBSOCKET_URL = () => `${baseURL}/websocket`;
let sock: WebSocket;
let stompClient: Client;

const MAX_RECONNECT_ATTEMPTS = 20;
const RECONNECT_WAIT_TIME = 5000;
let recInterval: NodeJS.Timeout;
let currentReconnectAttempts = 0;

/**
 * Returns singleton Stomp client or create new one if undefined.
 *
 * @param reconnect - Whether to create a new connection regardless
 * of websocket state.
 * @throws Throws errors if can't connect to server and reconnect is
 * not enabled.
 * @return The stomp client.
 */
function getStompClient(reconnect = false): Client {
  if (sock === undefined || stompClient === undefined || reconnect) {
    try {
      sock = new SockJS(WEBSOCKET_URL(), { DEBUG: false });
      sock.onclose = () => {
        logModule.onDevMessage("Closing WebSocket.");
        connect(MAX_RECONNECT_ATTEMPTS, RECONNECT_WAIT_TIME).then();
      };
      stompClient = Stomp.over(sock, { debug: false });
    } catch (e) {
      if (!reconnect) {
        throw e;
      }
    }
  }
  return stompClient;
}

/**
 * Connects to BEND websocket with a Stomp protocol and tries to reconnect if
 * the connection fails.
 *
 * @param maxReconnectAttempts - The number of times to try to reconnect before
 * failing.
 * @param reconnectWaitTime - The number of milliseconds to wait before attempting
 * reconnect
 * @param isReconnect - Whether this is a reconnect attempt.
 */
function connect(
  maxReconnectAttempts: number,
  reconnectWaitTime: number,
  isReconnect = false
): Promise<void> {
  return new Promise((resolve, reject) => {
    const stomp = getStompClient(isReconnect);
    if (stomp.connected) {
      logModule.onDevMessage("Client is connected to WebSocket.");
      clearInterval(recInterval);
      resolve();
    }

    if (currentReconnectAttempts > 0) {
      logModule.onDevMessage(
        `Websocket reconnect attempt:${currentReconnectAttempts}`
      );
    }

    currentReconnectAttempts++;
    stomp.connect(
      { host: WEBSOCKET_URL() },
      () => {
        if (currentReconnectAttempts > 1) {
          logModule.onSuccess("Web Socket reconnected to server.");
        }
        logModule.onDevMessage("Websocket connection successful.");
        clearInterval(recInterval);
        currentReconnectAttempts = 0;
        resolve();
      },
      () => {
        logModule.onDevMessage("Re-connecting with WebSocket.");
        clearInterval(recInterval);
        //TODO: Check if out of date during time disconnected.
        recInterval = setInterval(function () {
          if (currentReconnectAttempts < maxReconnectAttempts) {
            connect(maxReconnectAttempts, reconnectWaitTime, true)
              .then(resolve)
              .catch(reject);
          } else {
            clearInterval(recInterval);
            const error =
              "Web Socket lost connection to server, please reload page.";
            logModule.onError(error);
            reject(error);
          }
        }, reconnectWaitTime);
      }
    );
  });
}

/**
 * Clears all stomp client subscriptions.
 */
function clearSubscriptions() {
  const stomp = getStompClient();
  const subscriptionIds = Object.keys(stomp.subscriptions);

  subscriptionIds.forEach((subId) => stomp.unsubscribe(subId));
}

/**
 * Connects and subscribes to the given project and version.
 *
 * @param projectId - The project ID to connect to.
 * @param versionId - The project version ID to connect to.
 */
export function connectAndSubscribeToVersion(
  projectId: string,
  versionId: string
): Promise<void> {
  return new Promise((resolve, reject) => {
    if (!projectId || !versionId) {
      resolve();
      return;
    }

    connect(MAX_RECONNECT_ATTEMPTS, RECONNECT_WAIT_TIME)
      .then(() => {
        clearSubscriptions();
        const projectSubscription = `/topic/projects/${projectId}`;
        const versionSubscription = `/topic/revisions/${versionId}`;
        stompClient.subscribe(projectSubscription, async (frame) => {
          await projectMessageHandler(projectId, frame);
        });
        stompClient.subscribe(versionSubscription, async (frame) => {
          await versionMessageHandler(versionId, frame);
        });
        resolve();
      })
      .catch(reject);
  });
}

/**
 * Handles revision messages related to versioned entities of the project.
 *
 * @param versionId - The project version ID of the revision.
 * @param frame - The frame received by the version websocket channel.
 */
async function versionMessageHandler(
  versionId: string,
  frame: Frame
): Promise<void> {
  const message: VersionMessage = frame.body as VersionMessage;
  switch (message) {
    case "VERSION":
      return getProjectVersion(versionId).then(setCreatedProject);
    case "ARTIFACTS":
      //TODO: Updating with route to get artifacts in version.
      return getProjectVersion(versionId).then(setCreatedProject);
    case "TRACES":
      ///TODO: Updating with route to get traces in version.
      return getProjectVersion(versionId).then(setCreatedProject);
  }
}

/**
 * Handles revision messages.
 *
 * @param projectId - ID of project to update.
 * @param frame - The frame of the revision.
 */
async function projectMessageHandler(
  projectId: string,
  frame: Frame
): Promise<void> {
  const message: ProjectMessage = frame.body as ProjectMessage;
  switch (message) {
    case "MEMBERS":
      return getProjectMembers(projectId).then(projectModule.SET_MEMBERS);
    case "DOCUMENTS":
      return getProjectDocuments(projectId).then(projectModule.SET_DOCUMENTS);
  }
}
