package common;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.Test;

public abstract class AbstractCrudTest<T extends IAppEntity> extends ApplicationBaseTest {
    protected T entity;
    protected ProjectVersion projectVersion;
    protected Project project;
    protected UUID entityId;

    protected ProjectVersion setupProject() throws Exception {
        return creationTestService.createProjectWithNewVersion(projectName);
    }

    @Test
    public void testCrud() throws Exception {
        // Step - Setup project
        this.projectVersion = this.setupProject();
        this.project = this.projectVersion.getProject();
        notificationTestService.createNewConnection(defaultUser).subscribeToTopic(defaultUser, getTopicId());

        // Step - Create entity and retrieve message
        this.entityId = createEntity();
        assertThat(entityId).isNotNull();

        // VP - Verify created entity
        T entity = getEntity(projectVersion, entityId);
        verifyCreatedEntity(entity);

        // VP - Verify creation message
        EntityChangeMessage creationMessage = notificationTestService.getNextMessage(defaultUser);
        verifyCreationMessage(creationMessage);

        // Step - Update entity and retrieve message
        updateEntity();

        // Step - Verify updated entity
        T updatedEntity = getEntity(projectVersion, entityId);
        verifyUpdatedEntity(updatedEntity);

        // VP - Verify update message
        EntityChangeMessage updateMessage = notificationTestService.getNextMessage(defaultUser);
        verifyUpdateMessage(updateMessage);

        // Step - Delete entity
        deleteEntity(updatedEntity);

        // VP - Verify entity deleted
        List<T> entitiesWithId = getEntities(projectVersion, entityId);
        assertThat(entitiesWithId).isEmpty();

        // VP - Verify deletion message
        EntityChangeMessage deleteMessage = notificationTestService.getNextMessage(defaultUser);
        verifyDeletionMessage(deleteMessage);
    }

    private T getEntity(ProjectVersion projectVersion, UUID entityId) {
        return getEntities(projectVersion, entityId).get(0);
    }

    private List<T> getEntities(ProjectVersion projectVersion, UUID entityId) {
        return this.getAppService().getAppEntitiesByIds(projectVersion, List.of(entityId.toString()));
    }

    /**
     * @return {@link UUID} of topic to receive messages for entity changes.
     */
    protected abstract UUID getTopicId();

    /**
     * @return {@link IAppEntityService} Service for retrieving app entities being tested.
     */
    protected abstract IAppEntityService<T> getAppService();

    /**
     * Creates entity to be tested.
     *
     * @return {@link UUID} ID of entity created.
     * @throws Exception If HTTP error occurs
     */
    protected abstract UUID createEntity() throws Exception;

    /**
     * Verifies that given entity matches that created.
     *
     * @param retrievedEntity Entity created.
     */
    protected abstract void verifyCreatedEntity(T retrievedEntity);

    /**
     * Verifies the correctness of message received after entity is created.
     *
     * @param creationMessage {@link EntityChangeMessage} The message indicating entity was created.
     */
    protected abstract void verifyCreationMessage(EntityChangeMessage creationMessage);

    /**
     * Updates given app entity.
     *
     * @throws Exception If HTTP error occurs.
     */
    protected abstract void updateEntity() throws Exception;

    /**
     * Verifies that given entity contains updates specified.
     *
     * @param retrievedEntity Updated entity.
     */
    protected abstract void verifyUpdatedEntity(T retrievedEntity);

    /**
     * Verifies that message contains the update message for entity.
     *
     * @param updateMessage Message indicating that entity was updated
     */
    protected abstract void verifyUpdateMessage(EntityChangeMessage updateMessage);

    /**
     * Deletes given entity.
     *
     * @param entity The entity to delete
     * @throws Exception If HTTP error occurs.
     */
    protected abstract void deleteEntity(T entity) throws Exception;

    /**
     * Verifies content of message after entity is deleted.
     *
     * @param deletionMessage Message received after entity was deleted.
     */
    protected abstract void verifyDeletionMessage(EntityChangeMessage deletionMessage);
}
