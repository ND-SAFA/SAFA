package features.base;

import static java.util.concurrent.TimeUnit.SECONDS;

import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingDeque;

import edu.nd.crc.safa.config.WebSocketBrokerConfig;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.messaging.simp.stomp.StompFrameHandler;
import org.springframework.messaging.simp.stomp.StompHeaders;
import org.springframework.messaging.simp.stomp.StompSession;
import org.springframework.messaging.simp.stomp.StompSessionHandlerAdapter;
import org.springframework.web.socket.WebSocketHttpHeaders;
import org.springframework.web.socket.client.standard.StandardWebSocketClient;
import org.springframework.web.socket.messaging.WebSocketStompClient;
import org.springframework.web.socket.sockjs.client.SockJsClient;
import org.springframework.web.socket.sockjs.client.WebSocketTransport;

/**
 * Provides an abstraction over the websocket connection enabling:
 * 1. connecting to server through websocket endpoint
 * 2. Reading messages in queue associated
 * <p>
 * TODO: Do I need to clear subscriptions?
 */
public abstract class WebSocketBaseTest extends AuthenticatedBaseTest {

    static final String WEBSOCKET_URI = "ws://localhost:%s/websocket";
    private static ObjectMapper mapper;
    private static WebSocketStompClient stompClient;
    private static HashMap<String, BlockingQueue<String>> idToQueue;
    private static HashMap<String, StompSession> idToSession;

    final int TIME_TO_POLL_SECONDS = 10; // # of seconds to wait for a message until failing
    final int TIME_TO_POLL_MS = TIME_TO_POLL_SECONDS * 1000;

    @LocalServerPort
    private Integer port;

    @BeforeAll
    public static void setup() {
        mapper = new ObjectMapper();
        idToQueue = new HashMap<>();
        idToSession = new HashMap<>();
        StandardWebSocketClient webSocketClient = new StandardWebSocketClient();
        WebSocketTransport transport = new WebSocketTransport(webSocketClient);
        SockJsClient client = new SockJsClient(List.of(transport));
        stompClient = new WebSocketStompClient(client);
        stompClient.setInboundMessageSizeLimit(WebSocketBrokerConfig.MESSAGE_SIZE_LIMIT);
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
    public WebSocketBaseTest createNewConnection(String clientId) throws Exception {
        WebSocketHttpHeaders headers = new WebSocketHttpHeaders();
        StompSession session = stompClient
            .connect(String.format(WEBSOCKET_URI, port),
                new StompSessionHandlerAdapter() {
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
    public WebSocketBaseTest subscribeToProject(String clientId, Project project) {
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
    public WebSocketBaseTest subscribeToVersion(String clientId, ProjectVersion projectVersion) {
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
     * @param clientId    The Id of the client whose queue we're reading.
     * @param targetClass The target class which to map the message into.
     * @param <T>         The type of class to be returned.
     * @return
     * @throws InterruptedException    Throws error if problem occurs with thread when reading message.
     * @throws JsonProcessingException Throws error if cannot parse message into target class.
     */
    public <T> T getNextMessage(String clientId, Class<T> targetClass) throws InterruptedException, JsonProcessingException {
        String response = getNextMessage(clientId);
        assert response != null;
        return toClass(response, targetClass);
    }

    public <T> T toClass(String response, Class<T> targetClass) throws JsonProcessingException {
        return mapper.readValue(response, targetClass);
    }
    
    /**
     * Returns the next message in the queue associated with given client id.
     *
     * @param clientId The ID given to the client whose queue message is returned.
     * @return The next message in the queue.
     * @throws InterruptedException
     */
    public String getNextMessage(String clientId) throws InterruptedException {
        return idToQueue.get(clientId).poll(TIME_TO_POLL_SECONDS, SECONDS);
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

    private WebSocketBaseTest subscribe(String id, String topic) {
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
}
