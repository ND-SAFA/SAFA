package edu.nd.crc.safa.test.services.notifications;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.notifications.AcknowledgeMessage;
import edu.nd.crc.safa.features.notifications.AuthenticationMessage;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.services.MappingTestService;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class NotificationTestService {
    private static final ObjectMapper objectMapper = ObjectMapperConfig.create();
    private static final int MAX_POLL_TIME = 35; // # of seconds to wait for a message until failing
    private static final int MIN_POLL_TIME = 1;
    private final WebSocketServer server;

    public NotificationTestService(int port) {
        this.server = new WebSocketServer(port);
    }

    public List<EntityChangeMessage> getMessages(IUser user) throws InterruptedException {
        List<String> messagesRaw = this.server.getMessages(getClientId(user), MIN_POLL_TIME);
        return messagesRaw
            .stream()
            .map(m -> MappingTestService.toClass(m, EntityChangeMessage.class))
            .peek(this::convertTypes)
            .collect(Collectors.toList());
    }

    public EntityChangeMessage getEntityMessage(IUser user) throws JsonProcessingException,
        InterruptedException {
        EntityChangeMessage message = getNextMessage(getClientId(user), EntityChangeMessage.class);
        convertTypes(message);
        return message;
    }


    /**
     * Clears all web socket sessions.
     */
    public void clearServer() {
        this.server.clear();
    }

    /**
     * Clears messages for user.
     *
     * @param user The user to clear messages for.
     */
    public void clearQueue(IUser user) {
        this.server.clearQueue(getClientId(user));
    }

    /**
     * Starts session for user and authenticates them.
     *
     * @param user  The user starting to start session for.
     * @param token The user's authorization token.
     * @throws Exception If error occurs during network or parsing of messages.
     */
    public void initializeUser(IUser user, String token) throws Exception {
        this.startSession(user);
        this.authenticate(user, token);
    }

    /**
     * Authenticates user, storing credentials in web socket session.
     *
     * @param user  The user to authenticate.
     * @param token The JWT token to authenticate user with.
     * @throws JsonProcessingException If error occurs while serializing authentication message.
     * @throws InterruptedException    If interrupted during network calls.
     */
    public void authenticate(IUser user, String token) throws JsonProcessingException, InterruptedException {
        AuthenticationMessage authMessage = new AuthenticationMessage(token);
        UUID clientId = getClientId(user);
        this.send(clientId, TopicCreator.getAuthenticationTopic(), authMessage);
        AcknowledgeMessage ack = getNextMessage(clientId, AcknowledgeMessage.class);
        assertEquals("OK", ack.getMessage());
    }

    /**
     * Subscribes client with associated id to the given project.
     *
     * @param user    The user subscribing to project updates.
     * @param project The project to listen updates to.
     * @return The test instance allowing for the builder pattern.
     */
    public NotificationTestService subscribeToProject(IUser user, Project project) {
        String projectTopic = TopicCreator.getProjectTopic(project.getProjectId());
        this.server.subscribe(getClientId(user), projectTopic);
        return this;
    }

    /**
     * Subscribes client with associated id to the given project version.
     *
     * @param user           The user subscribing to project version.
     * @param projectVersion The project version to listen updates to.
     * @return The test instance allowing for the builder pattern.
     */
    public NotificationTestService subscribeToVersion(IUser user, ProjectVersion projectVersion) {
        String versionTopic = TopicCreator.getVersionTopic(projectVersion.getVersionId());
        this.server.subscribe(getClientId(user), versionTopic);
        return this;
    }

    /**
     * Subscribes client with associated id to the given project version.
     *
     * @param user        The user subscribing to project version updates.
     * @param jobDbEntity The job whose updates are listened for.
     */
    public void subscribeToJob(IUser user, JobDbEntity jobDbEntity) {
        String jobTopic = TopicCreator.getJobTopic(jobDbEntity.getId());
        this.server.subscribe(getClientId(user), jobTopic);
    }

    /**
     * Subscribes to user topic. Enables receiving private messages.
     *
     * @param user The user subscribing to topic.
     */
    public void subscribeToUser(IUser user) {
        String projectVersionSubscriptionDestination = TopicCreator.getUserTopic(user);
        this.server.subscribe(getClientId(user), projectVersionSubscriptionDestination);
    }

    /**
     * Subscribes user to given topic.
     *
     * @param user  The user receiving topic messages.
     * @param topic The topic to subscribe to.
     */
    public void subscribe(IUser user, String topic) {
        this.server.subscribe(getClientId(user), topic);
    }

    /**
     * Returns the number of messages in the websocket queue.
     *
     * @param user The client whose queue we're reading.
     * @return int representing the number of messages in the queue.
     * @throws InterruptedException Throws error if some thread error occurs.
     */
    public int getQueueSize(IUser user) throws InterruptedException {
        return this.server.getQueue(getClientId(user), MAX_POLL_TIME).size();
    }

    /**
     * Sends message from client to destination.
     *
     * @param clientId    The client sending the message.
     * @param destination The destination of the message.
     * @param object      The object to be passed in message.
     * @throws JsonProcessingException Error if object serialization fails.
     */
    public void send(UUID clientId, String destination, Object object) throws JsonProcessingException {
        this.server.send(clientId, destination, object);
    }

    private void startSession(IUser user) throws Exception {
        this.server.connect(getClientId(user));
        this.subscribeToUser(user);
    }

    private <T> T getNextMessage(UUID clientId, Class<T> classType) throws JsonProcessingException,
        InterruptedException {
        String response = this.server.getMessage(clientId, MAX_POLL_TIME);
        assert response != null;
        return MappingTestService.toClass(response, classType);
    }

    private UUID getClientId(IUser user) {
        return user.getUserId();
    }

    private void convertTypes(EntityChangeMessage message) {
        message.getChanges().forEach(c -> {
            Class changeType = getChangeClass(c.getEntity());
            List<Object> entities = c.getEntities()
                .stream()
                .map(e -> objectMapper.convertValue(e, changeType))
                .collect(Collectors.toList());
            c.setEntities(entities);
        });
    }

    private Class getChangeClass(NotificationEntity entity) {
        return switch (entity) {
            case ACTIVE_MEMBERS -> UserAppEntity.class;
            case PROJECT -> Project.class;
            case MEMBERS -> UserAppEntity.class;
            case VERSION -> ProjectVersion.class;
            case TYPES -> ArtifactType.class;
            case DOCUMENT -> DocumentAppEntity.class;
            case ARTIFACTS -> ArtifactAppEntity.class;
            case TRACES -> TraceAppEntity.class;
            case JOBS -> JobAppEntity.class;
            case TRACE_MATRICES -> TraceMatrixAppEntity.class;
            default -> String.class;
        };
    }
}
