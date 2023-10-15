package edu.nd.crc.safa.test.common;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.google.errorprone.annotations.ForOverride;
import org.junit.jupiter.api.Test;

public abstract class AbstractCrudTest<T extends IAppEntity> extends ApplicationBaseTest {
    protected T entity;
    protected ProjectVersion projectVersion;
    protected Project project;
    protected UUID entityId;

    protected ProjectVersion setupProject() throws Exception {
        return this.rootBuilder
            .log("Creating project and initial version under root user.")
            .actions(a -> a.createProjectWithVersion(getCurrentUser())).get();
    }

    @Test
    public void testCrud() throws Exception {
        // Step - Setup project
        this.projectVersion = this.setupProject();
        this.project = this.projectVersion.getProject();
        this.dbEntityBuilder.setProject(projectName, this.project);

        this.rootBuilder
            .log("Root User: Subscribing to entity topic.")
            .notifications(n -> n.initializeUser(getCurrentUser(), getToken(getCurrentUser())).subscribe(getCurrentUser(), getTopic()));

        // Verifies any messages related to subscribing to topic (e.g. active members).
        onPostSubscribe();

        // Step - Create entity and retrieve message
        this.entityId = createEntity();
        assertThat(entityId).isNotNull();

        // VP - Verify created entity
        T entity = getEntity(projectVersion, getCurrentUser(), entityId);
        verifyCreatedEntity(entity);

        List<EntityChangeMessage> creationMessages = this.rootBuilder.notifications(n -> n.getMessages(getCurrentUser())).get();
        this.verifyCreationMessages(creationMessages);

        // Step - Update entity and retrieve message
        updateEntity();

        List<EntityChangeMessage> updateMessages =
            this.rootBuilder.notifications(n -> n.getMessages(getCurrentUser())).get();


        // Step - Verify updated entity
        T updatedEntity = getEntity(projectVersion, getCurrentUser(), entityId);
        verifyUpdatedEntity(updatedEntity);

        // VP - Verify update message
        this.verifyUpdateMessages(updateMessages);

        // Step - Delete entity
        deleteEntity(updatedEntity);

        List<EntityChangeMessage> deletedMessages =
            this.rootBuilder.notifications(n -> n.getMessages(getCurrentUser())).get();


        // VP - Verify entity deleted
        List<T> entitiesWithId = getEntities(projectVersion, getCurrentUser(), entityId);
        assertThat(entitiesWithId).isEmpty();

        // VP - Verify deletion message
        verifyDeletionMessages(deletedMessages);
    }

    private T getEntity(ProjectVersion projectVersion, SafaUser user, UUID entityId) {
        return getEntities(projectVersion, user, entityId).get(0);
    }

    private List<T> getEntities(ProjectVersion projectVersion, SafaUser user, UUID entityId) {
        return this.getAppService().getAppEntitiesByIds(projectVersion, user, List.of(entityId));
    }

    @ForOverride
    protected void onPostSubscribe() throws Exception {
    }

    /**
     * @return {@link UUID} of topic to receive messages for entity changes.
     */
    protected abstract List<String> getTopic();

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
     * @param messages {@link EntityChangeMessage} The messages received after entity was created.
     */
    protected abstract void verifyCreationMessages(List<EntityChangeMessage> messages);

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
     * @param messages Messages received after updating entity.
     */
    protected abstract void verifyUpdateMessages(List<EntityChangeMessage> messages);

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
     * @param messages Messages received after entity deleted.
     */
    protected abstract void verifyDeletionMessages(List<EntityChangeMessage> messages);
}
