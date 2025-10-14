package edu.nd.crc.safa.test.services.notifications;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.types.entities.TypeAppEntity;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.services.MappingTestService;
import edu.nd.crc.safa.test.services.builders.BuilderState;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class NotificationTestService {
    private static final ObjectMapper objectMapper = ObjectMapperConfig.create();
    private static final int MAX_POLL_TIME = 35; // # of seconds to wait for a message until failing
    private static final int MIN_POLL_TIME = 1;
    private final BuilderState state;
    private final WebSocketServer server;

    public NotificationTestService(BuilderState state, int port) {
        this.server = new WebSocketServer(port); // TODO: Does server go in state?
        this.state = state;
    }

    public List<EntityChangeMessage> getMessages(IUser user) {
        List<String> messagesRaw = this.server.getMessages(getClientId(user), MAX_POLL_TIME);
        List<EntityChangeMessage> messages = messagesRaw
            .stream()
            .map(m -> MappingTestService.toClass(m, EntityChangeMessage.class))
            .peek(this::convertTypes)
            .collect(Collectors.toList());
        this.clearQueue(user);
        return messages;
    }

    public EntityChangeMessage getEntityMessage(IUser user) {
        try {
            EntityChangeMessage message = getNextMessage(getClientId(user), EntityChangeMessage.class);
            convertTypes(message);
            return message;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }


    /**
     * Clears all web socket sessions.
     */
    public NotificationTestService clearServer() {
        this.server.clear();
        return this;
    }

    /**
     * Clears messages for user.
     *
     * @param user The user to clear messages for.
     */
    public NotificationTestService clearQueue(IUser user) {
        this.server.clearQueue(getClientId(user));
        return this;
    }

    /**
     * Starts session for user and authenticates them.
     *
     * @param user  The user starting to start session for.
     * @param token The user's authorization token.
     * @throws Exception If error occurs during network or parsing of messages.
     */
    public NotificationTestService initializeUser(IUser user, String token) {
        try {
            this.startSession(user, token);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        return this;
    }

    /**
     * Subscribes client with associated id to the given project.
     *
     * @param user The user subscribing to project updates.
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
    public NotificationTestService subscribeToJob(IUser user, JobDbEntity jobDbEntity) {
        String jobTopic = TopicCreator.getJobTopic(jobDbEntity.getId());
        this.server.subscribe(getClientId(user), jobTopic);
        return this;
    }

    public NotificationTestService subscribe(IUser user, List<String> topics) {
        UUID clientId = getClientId(user);
        topics.forEach(t -> this.server.subscribe(clientId, t));
        return this;
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

    private void startSession(IUser user, String token) throws Exception {
        this.server.connect(getClientId(user), token);
    }

    private <T> T getNextMessage(UUID clientId, Class<T> classType) throws JsonProcessingException,
        InterruptedException {
        String response = this.server.getMessage(clientId, MAX_POLL_TIME);
        assert response != null : "No message for client: " + clientId;
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
            case TYPES -> TypeAppEntity.class;
            case DOCUMENT -> DocumentAppEntity.class;
            case ARTIFACTS -> ArtifactAppEntity.class;
            case TRACES -> TraceAppEntity.class;
            case JOBS -> JobAppEntity.class;
            case TRACE_MATRICES -> TraceMatrixAppEntity.class;
            case WARNINGS -> String.class;
            default -> throw new RuntimeException("No conversion class registered for: " + entity);
        };
    }
}
