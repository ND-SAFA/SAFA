package edu.nd.crc.safa.features.types.services;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.TypeAppEntity;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.types.entities.db.ArtifactTypeCount;
import edu.nd.crc.safa.features.types.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.services.VersionService;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for retrieving {@link TypeAppEntity}.
 */
@AllArgsConstructor
@Service
public class TypeService implements IAppEntityService<TypeAppEntity> {
    private ArtifactTypeRepository artifactTypeRepository;
    private ArtifactRepository artifactRepository;
    private NotificationService notificationService;
    private ArtifactTypeCountService typeCountService;
    private VersionService versionService;

    @Override
    public List<TypeAppEntity> getAppEntities(ProjectVersion projectVersion, SafaUser user) {
        List<TypeAppEntity> types = getAppEntities(projectVersion.getProject());
        attachTypeCounts(projectVersion, types);
        return types;
    }

    public List<TypeAppEntity> getAppEntities(Project project) {
        return getTypes(project)
            .stream()
            .map(TypeAppEntity::new)
            .collect(Collectors.toList());
    }

    private void attachTypeCounts(ProjectVersion projectVersion, List<TypeAppEntity> types) {
        // Doing it this way allows us to reduce database calls which is faster
        Map<UUID, TypeAppEntity> typeMap = new HashMap<>();
        types.forEach(type -> typeMap.put(type.getId(), type));

        List<ArtifactTypeCount> counts = typeCountService.getByProjectVersion(projectVersion);
        for (ArtifactTypeCount count : counts) {
            typeMap.get(count.getType().getId()).setCount(count.getCount());
        }
    }

    /**
     * Get all types within a project.
     *
     * @param project The project
     * @return The types in the project
     */
    public List<ArtifactType> getTypes(Project project) {
        return artifactTypeRepository.findByProject(project);
    }

    /**
     * Get the artifact type by its id.
     *
     * @param artifactTypeId the id of the artifact type
     * @return the artifact type, or null if it was not found
     */
    public ArtifactType getArtifactType(UUID artifactTypeId) {
        return artifactTypeRepository.findById(artifactTypeId).orElse(null);
    }

    /**
     * Get and artifact type for a given project by its name.
     *
     * @param project the project the type belongs to
     * @param artifactTypeName the name of the artifact type
     * @return the artifact type, or null if it was not found
     */
    public ArtifactType getArtifactType(Project project, String artifactTypeName) {
        return artifactTypeRepository.findByProjectAndNameIgnoreCase(project, artifactTypeName).orElse(null);
    }

    /**
     * Save an artifact type.
     *
     * @param artifactType the artifact type to save
     * @return the saved artifact type
     */
    public ArtifactType saveArtifactType(ArtifactType artifactType) {
        return artifactTypeRepository.save(artifactType);
    }

    /**
     * Create an artifact type for a given project.
     *
     * @param project the project the type belongs to
     * @param name the name of the artifact type
     * @param user The user doing the operation
     * @return the created artifact type
     */
    public ArtifactType createArtifactType(Project project, String name, SafaUser user) {
        return createArtifactType(new ArtifactType(project, name), user);
    }

    /**
     * Create an artifact type for a given project.
     *
     * @param project the project the type belongs to
     * @param name the name of the artifact type
     * @param color the color associated with the type
     * @param user The user doing the operation
     * @return the created artifact type
     */
    public ArtifactType createArtifactType(Project project, String name, String color, SafaUser user) {
        return createArtifactType(new ArtifactType(project, name, color), user);
    }

    /**
     * Save an artifact type to the database with some error checking and notifications.
     *
     * @param artifactType The type we are creating
     * @param user The user doing the operation
     * @return The type that got saved to the database
     */
    private ArtifactType createArtifactType(ArtifactType artifactType, SafaUser user) {
        ArtifactType existingType = getArtifactType(artifactType.getProject(), artifactType.getName());
        if (existingType != null) {
            throw new SafaError("Type exists: " + artifactType.getName());
        }

        artifactType = saveArtifactType(artifactType);

        createTypeCounts(artifactType);

        notifyTypeUpdate(artifactType, user);

        return artifactType;
    }

    /**
     * Create type count objects for this type for all existing versions in a project.
     *
     * @param artifactType The type we are counting
     */
    private void createTypeCounts(ArtifactType artifactType) {
        Project project = artifactType.getProject();
        for (ProjectVersion projectVersion : versionService.getProjectVersions(project)) {
            ArtifactTypeCount typeCount = new ArtifactTypeCount(projectVersion, artifactType);
            typeCountService.save(typeCount);
        }
    }

    /**
     * Update values in an artifact type.
     *
     * @param project Project containing the type
     * @param updatedArtifactType The updated type definition
     * @param user The user doing the operation
     * @return The type after the update (may not match the passed in type 100% as we do not allow editing
     *         certain values)
     */
    public ArtifactType updateArtifactType(Project project, ArtifactType updatedArtifactType, SafaUser user) {
        ArtifactType originalType = getArtifactType(project, updatedArtifactType.getName());

        if (originalType == null) {
            throw new SafaItemNotFoundError(updatedArtifactType.getName());
        }

        // Don't allow editing the id or project
        updatedArtifactType.setId(originalType.getId());
        updatedArtifactType.setProject(originalType.getProject());

        updatedArtifactType = saveArtifactType(updatedArtifactType);

        notifyTypeUpdate(updatedArtifactType, user);

        return updatedArtifactType;
    }

    /**
     * Delete a type
     *
     * @param type The type to delete
     * @param user The user doing the operation
     */
    public void deleteArtifactType(ArtifactType type, SafaUser user) {
        artifactTypeRepository.delete(type);
        notifyTypeDeleted(type, user);
    }

    private void notifyTypeUpdate(ArtifactType artifactType, SafaUser user) {
        Project project = artifactType.getProject();

        // Step - Calculate affected artifact ids
        List<UUID> artifactIds = artifactRepository
            .findByProjectAndType(project, artifactType)
            .stream()
            .map(Artifact::getArtifactId)
            .collect(Collectors.toList());

        // Step - broadcast change to artifact type and affected artifacts
        notificationService.broadcastChangeToUser(
            EntityChangeBuilder.create(project.getProjectId())
                .withTypeUpdate(artifactType.getId())
                .withArtifactsUpdate(artifactIds), user);
    }

    private void notifyTypeDeleted(ArtifactType artifactType, SafaUser user) {
        notificationService.broadcastChangeToUser(
            EntityChangeBuilder
                .create(artifactType.getProject().getProjectId())
                .withTypeDelete(artifactType.getId())
                .withUpdateLayout(), user);
    }

    public void deleteAll() {
        artifactTypeRepository.deleteAll();
    }
}
