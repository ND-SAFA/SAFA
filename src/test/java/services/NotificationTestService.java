package services;

import static java.util.concurrent.TimeUnit.SECONDS;

import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingDeque;

import edu.nd.crc.safa.config.WebSocketBrokerConfig;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.messaging.simp.stomp.StompFrameHandler;
import org.springframework.messaging.simp.stomp.StompHeaders;
import org.springframework.messaging.simp.stomp.StompSession;
import org.springframework.messaging.simp.stomp.StompSessionHandlerAdapter;
import org.springframework.web.socket.WebSocketHttpHeaders;
import org.springframework.web.socket.client.standard.StandardWebSocketClient;
import org.springframework.web.socket.messaging.WebSocketStompClient;
import org.springframework.web.socket.sockjs.client.SockJsClient;
import org.springframework.web.socket.sockjs.client.WebSocketTransport;

public class NotificationTestService {

    private final WebSocketStompClient stompClient;
    private final HashMap<String, StompSession> idToSession = new HashMap<>();
    private final int port;
    private HashMap<String, BlockingQueue<String>> idToQueue = new HashMap<>();

    public NotificationTestService(int port) {
        this.stompClient = createStompClient();
        this.port = port;
    }

    private WebSocketStompClient createStompClient() {
        StandardWebSocketClient webSocketClient = new StandardWebSocketClient();
        WebSocketTransport transport = new WebSocketTransport(webSocketClient);
        SockJsClient client = new SockJsClient(List.of(transport));
        WebSocketStompClient stompClient = new WebSocketStompClient(client);
        stompClient.setInboundMessageSizeLimit(WebSocketBrokerConfig.MESSAGE_SIZE_LIMIT);
        return stompClient;
    }

    @BeforeEach
    public void clearQueue() {
        idToQueue = new HashMap<>();
    }

    /**
     * Creates a new stomp session and stores connection for given client id.
     *
     * @param clientId User specified unique identifier for a client.
     * @return Current object allowing for builder pattern.
     * @throws Exception Throws error if a problem occurs connecting to stomp endpoint.
     */
    public NotificationTestService createNewConnection(String clientId) throws Exception {
        WebSocketHttpHeaders headers = new WebSocketHttpHeaders();
        StompSession session = stompClient
            .connect(String.format(Constants.WEBSOCKET_URI, port), new StompSessionHandlerAdapter() {
            })
            .get(1, SECONDS);
        idToSession.put(clientId, session);
        idToQueue.put(clientId, new LinkedBlockingDeque<>());
        return this;
    }

    /**
     * Subscribes client with associated id to the given project.
     *
     * @param clientId The ID given to client subscribing to project version.
     * @param project  The project to listen updates to.
     * @return The test instance allowing for the builder pattern.
     */
    public NotificationTestService subscribeToProject(String clientId, Project project) {
        String projectSubscriptionDestination = NotificationService.getTopic(project.getProjectId());
        return this.subscribe(clientId, projectSubscriptionDestination);
    }

    /**
     * Subscribes client with associated id to the given project version.
     *
     * @param clientId       The ID given to client subscribing to project version.
     * @param projectVersion The project version to listen updates to.
     * @return The test instance allowing for the builder pattern.
     */
    public NotificationTestService subscribeToVersion(String clientId, ProjectVersion projectVersion) {
        String projectVersionSubscriptionDestination = NotificationService.getTopic(projectVersion.getVersionId());
        return this.subscribe(clientId, projectVersionSubscriptionDestination);
    }

    /**
     * Subscribes client with associated id to the given project version.
     *
     * @param clientId    The ID given to client subscribing to project version.
     * @param jobDbEntity The job whose updates are listened for.
     */
    public void subscribeToJob(String clientId, JobDbEntity jobDbEntity) {
        String projectVersionSubscriptionDestination = NotificationService.getTopic(jobDbEntity.getId());
        this.subscribe(clientId, projectVersionSubscriptionDestination);
    }

    /**
     * Returns the next message in the queue associated with given client id.
     *
     * @param clientId The ID of the client whose queue we're reading.
     * @return {@link EntityChangeMessage} Message is client's queue.
     * @throws InterruptedException    Throws error if problem occurs with thread when reading message.
     * @throws JsonProcessingException Throws error if cannot parse message into target class.
     */
    public EntityChangeMessage getNextMessage(String clientId) throws JsonProcessingException, InterruptedException {
        String response = getMessageInQueue(clientId);
        assert response != null;
        return MappingTestService.toClass(response, EntityChangeMessage.class);
    }

    /**
     * Returns the next message in the queue associated with given client id.
     *
     * @param clientId The ID given to the client whose queue message is returned.
     * @return The next message in the queue.
     * @throws InterruptedException If interrupted while polling for message.
     */
    private String getMessageInQueue(String clientId) throws InterruptedException {
        return idToQueue.get(clientId).poll(Constants.TIME_TO_POLL_SECONDS, SECONDS);
    }

    /**
     * Returns the number of messages in the websocket queue.
     *
     * @param clientId The id given to the client whose queue we're reading.
     * @return int representing the number of messages in the queue.
     * @throws InterruptedException Throws error if some thread error occurs.
     */
    public int getQueueSize(String clientId) throws InterruptedException {
        Thread.sleep(750);
        return idToQueue.get(clientId).size();
    }

    private NotificationTestService subscribe(String id, String topic) {
        idToSession.get(id).subscribe(topic, new StompFrameHandler() {
            public Type getPayloadType(StompHeaders stompHeaders) {
                return byte[].class;
            }

            public void handleFrame(StompHeaders stompHeaders, Object o) {
                idToQueue.get(id).offer(new String((byte[]) o));
            }
        });
        return this;
    }

    static class Constants {
        private static final String WEBSOCKET_URI = "ws://localhost:%s/websocket";
        private static final int TIME_TO_POLL_SECONDS = 10; // # of seconds to wait for a message until failing
    }
}
