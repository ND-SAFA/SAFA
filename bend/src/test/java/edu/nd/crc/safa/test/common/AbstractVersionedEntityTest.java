package edu.nd.crc.safa.test.common;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.features.common.IVersionEntity;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

import org.javatuples.Pair;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * Tests that versioned entities are correctly tracked across different forms of
 * modification.
 *
 * @param <T>  AppEntity data type
 * @param <TV> Versioned data type
 */
public abstract class AbstractVersionedEntityTest<T extends IAppEntity, TV extends IVersionEntity<T>>
    extends ApplicationBaseTest {

    protected TV entity;
    protected ProjectVersion projectV1;
    protected ProjectVersion projectV2;
    protected Project project;

    @BeforeEach
    public void setup() throws Exception {
        Pair<ProjectVersion, ProjectVersion> projectVersions = setupProject();
        projectV1 = projectVersions.getValue0();
        projectV2 = projectVersions.getValue1();
        project = projectV1.getProject();

        loadDataIntoProjectVersion(projectV1);
        loadDataIntoProjectVersion(projectV2);

        List<TV> allVersions = getAllVersions(project);
        assertThat(allVersions).hasSize(1);
        entity = allVersions.get(0);
    }

    /**
     * Tests that when no change is made to an entity, no change is recorded in the versioning system.
     */
    @Test
    public void testNoChanges() {
        Optional<TV> entityInV1 = getEntityVersionByProjectVersion(entity, projectV1);
        assertThat(entityInV1).isPresent();
        assertThat(entityInV1.get().getModificationType()).isEqualTo(ModificationType.ADDED);

        Optional<TV> entityInV2 = getEntityVersionByProjectVersion(entity, projectV2);
        assertThat(entityInV2).isNotPresent();
    }

    /**
     * Tests that when a change is made to an entity in V1 of a project, only V1 is updated.
     *
     * @throws Exception When committing a change fails
     */
    @Test
    public void testChangeInV1() throws Exception {
        commitChangeToEntityInVersion(entity, projectV1, this::modifyEntityInCommit);

        Optional<TV> entityInV1 = getEntityVersionByProjectVersion(entity, projectV1);
        assertThat(entityInV1).isPresent();
        verifyChangeToEntity(entityInV1.get());

        Optional<TV> entityInV2 = getEntityVersionByProjectVersion(entity, projectV2);
        assertThat(entityInV2).isNotPresent();
    }

    /**
     * Tests that when a change is made to an entity in V2 of a project, V1 is not updated,
     * and V2 contains the modification.
     *
     * @throws Exception When committing a change fails
     */
    @Test
    public void testChangeInV2() throws Exception {
        commitChangeToEntityInVersion(entity, projectV2, this::modifyEntityInCommit);

        Optional<TV> entityInV1 = getEntityVersionByProjectVersion(entity, projectV1);
        assertThat(entityInV1).isPresent();
        verifyNoChangeToEntity(entityInV1.get());

        Optional<TV> entityInV2 = getEntityVersionByProjectVersion(entity, projectV2);
        assertThat(entityInV2).isPresent();
        verifyChangeToEntity(entityInV2.get());
    }

    /**
     * Tests that when an entity is removed from V1 of a project, it is not present
     * in either version.
     *
     * @throws Exception When committing a change fails
     */
    @Test
    public void testDeleteInV1() throws Exception {
        commitChangeToEntityInVersion(entity, projectV1, this::removeEntityInCommit);

        Optional<TV> entityInV1 = getEntityVersionByProjectVersion(entity, projectV1);
        assertThat(entityInV1).isPresent();
        assertThat(entityInV1.get().getModificationType()).isEqualTo(ModificationType.REMOVED);

        Optional<TV> entityInV2 = getEntityVersionByProjectVersion(entity, projectV2);
        assertThat(entityInV2).isNotPresent();
    }

    /**
     * Tests that when an entity is removed from V2 of a project, it is still present in
     * V1, and marked as deleted in V2.
     *
     * @throws Exception When committing a change fails
     */
    @Test
    public void testDeleteInV2() throws Exception {
        commitChangeToEntityInVersion(entity, projectV2, this::removeEntityInCommit);

        Optional<TV> entityInV1 = getEntityVersionByProjectVersion(entity, projectV1);
        assertThat(entityInV1).isPresent();
        assertThat(entityInV1.get().getModificationType()).isEqualTo(ModificationType.ADDED);

        Optional<TV> entityInV2 = getEntityVersionByProjectVersion(entity, projectV2);
        assertThat(entityInV2).isPresent();
        assertThat(entityInV2.get().getModificationType()).isEqualTo(ModificationType.REMOVED);
    }

    /**
     * Creates a new project with 2 versions.
     *
     * @return V1 and V2 of the project
     */
    protected Pair<ProjectVersion, ProjectVersion> setupProject() {
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);

        ProjectVersion beforeVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion afterVersion = dbEntityBuilder.getProjectVersion(projectName, 1);

        return new Pair<>(beforeVersion, afterVersion);
    }

    /**
     * Applies a generic change to an entity based on the changeFunction and then commits it to
     * the project version.
     *
     * @param entity         The entity to change
     * @param projectVersion The version in which to make the change
     * @param changeFunction The function to use to apply the change
     * @throws Exception When committing a change fails
     */
    private void commitChangeToEntityInVersion(TV entity, ProjectVersion projectVersion,
                                               ChangeEntityForCommit<T, TV> changeFunction) throws Exception {
        CommitBuilder commitBuilder = CommitBuilder.withVersion(projectVersion);
        changeFunction.applyChange(commitBuilder, entity);
        commitService.commit(commitBuilder);
    }

    /**
     * Loads data necessary for testing into a given version of a project, e.g. by loading from
     * a flat file directory.
     *
     * @param projectVersion The version of the project to load the data into.
     * @throws Exception When loading data fails
     */
    protected abstract void loadDataIntoProjectVersion(ProjectVersion projectVersion) throws Exception;

    /**
     * Retrieves all versions of the entity under test that exist within the given project.
     *
     * @param project The project to look in.
     * @return All versions of the test entity.
     */
    protected abstract List<TV> getAllVersions(Project project);

    /**
     * Retrieves the version of the given entity associated with the given project version. This
     * may or may not exist depending on whether some form of modification to the entity was
     * applied in that project version.
     *
     * @param entity         The entity in question
     * @param projectVersion The project version to look in
     * @return The entity in the given project version, if it exists
     */
    protected abstract Optional<TV> getEntityVersionByProjectVersion(TV entity, ProjectVersion projectVersion);

    /**
     * Applies a modification to a particular entity and stores it within the commit builder to be
     * committed.
     *
     * @param commitBuilder A builder for the commit that will be applied
     * @param entity        The entity to modify
     */
    protected abstract void modifyEntityInCommit(CommitBuilder commitBuilder, TV entity);

    /**
     * Stores the removal of a particular entity within the commit builder.
     *
     * @param commitBuilder A builder for the commit that will be applied
     * @param entity        The entity to remove
     */
    protected abstract void removeEntityInCommit(CommitBuilder commitBuilder, TV entity);

    /**
     * Verifies that the change applied by modifyEntityInCommit() is present in the given entity.
     *
     * @param entity The entity to check
     */
    protected abstract void verifyChangeToEntity(TV entity);

    /**
     * Verifies that the change applied by modifyEntityInCommit() is not present in the given entity.
     *
     * @param entity The entity to check
     */
    protected abstract void verifyNoChangeToEntity(TV entity);

    /**
     * Used to condense code for committing changes to a project version.
     *
     * @param <T>  Entity type
     * @param <TV> Entity version type
     */
    @FunctionalInterface
    private interface ChangeEntityForCommit<T extends IAppEntity, TV extends IVersionEntity<T>> {
        void applyChange(CommitBuilder commitBuilder, TV entity);
    }

}
