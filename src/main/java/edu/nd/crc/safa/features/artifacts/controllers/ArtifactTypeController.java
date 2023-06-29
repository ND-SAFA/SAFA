package edu.nd.crc.safa.features.artifacts.controllers;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.ArtifactType;
import edu.nd.crc.safa.features.types.TypeAppEntity;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for calculating the changes between two project versions.
 */
@RestController
public class ArtifactTypeController extends BaseController {

    @Autowired
    public ArtifactTypeController(ResourceBuilder resourceBuilder,
                                  ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Creates given artifact type entity on specified project.
     *
     * @param projectId    The id of the project whose type is created for.
     * @param artifactType The artifact type to create.
     * @return The updated artifact type with id.
     * @throws SafaError Throws error if user does not have edit permissions on project.
     */
    @PostMapping(AppRoutes.ArtifactType.CREATE_ARTIFACT_TYPE)
    public TypeAppEntity createArtifactType(@PathVariable UUID projectId,
                                            @RequestBody ArtifactType artifactType) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();

        Optional<ArtifactType> originalType = this.serviceProvider.getArtifactTypeRepository()
            .findByProjectAndNameIgnoreCase(project, artifactType.getName());

        if (originalType.isPresent()) {
            throw new SafaError("Type exists: " + artifactType.getName());
        }

        // Don't trust values sent to us
        artifactType.setProject(project);
        artifactType.setTypeId(null);

        this.serviceProvider.getArtifactTypeRepository().save(artifactType);

        notifyTypeUpdate(project, artifactType);

        return new TypeAppEntity(artifactType);
    }

    /**
     * Updates given artifact type entity on specified project.
     *
     * @param projectId    The id of the project whose type is updated for.
     * @param artifactType The type we're updating
     * @param artifactTypeObj The value for the update.
     * @return The updated artifact type.
     * @throws SafaError Throws error if user does not have edit permissions on project.
     */
    @PutMapping(AppRoutes.ArtifactType.UPDATE_ARTIFACT_TYPE)
    public TypeAppEntity updateArtifactType(@PathVariable UUID projectId, @PathVariable String artifactType,
                                            @RequestBody ArtifactType artifactTypeObj) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();

        Optional<ArtifactType> originalType = this.serviceProvider.getArtifactTypeRepository()
            .findByProjectAndNameIgnoreCase(project, artifactType);

        if (originalType.isEmpty()) {
            throw new SafaItemNotFoundError(artifactType);
        }

        // Don't allow editing the type or project
        artifactTypeObj.setTypeId(originalType.get().getTypeId());
        artifactTypeObj.setProject(originalType.get().getProject());

        this.serviceProvider.getArtifactTypeRepository().save(artifactTypeObj);

        notifyTypeUpdate(project, artifactTypeObj);

        return new TypeAppEntity(artifactTypeObj);
    }

    private void notifyTypeUpdate(Project project, ArtifactType artifactType) {
        // Step - Calculate affected artifact ids
        List<UUID> artifactIds = this.serviceProvider
            .getArtifactRepository()
            .findByProjectAndType(project, artifactType)
            .stream()
            .map(Artifact::getArtifactId)
            .collect(Collectors.toList());

        // Step - broadcast change to artifact type and affected artifacts
        this.serviceProvider
            .getNotificationService()
            .broadcastChange(
                EntityChangeBuilder
                    .create(project.getProjectId())
                    .withTypeUpdate(artifactType.getTypeId())
                    .withArtifactsUpdate(artifactIds));
    }

    /**
     * Deletes the artifact type with specified type id.
     *
     * @param typeId The id of the type to delete.
     * @throws SafaError Throws error if user does not have edit permissions on project.
     */
    @DeleteMapping(AppRoutes.ArtifactType.DELETE_ARTIFACT_TYPE)
    public void deleteArtifactType(@PathVariable UUID typeId) throws SafaError {
        ArtifactTypeRepository artifactTypeRepository = this.serviceProvider.getArtifactTypeRepository();
        ArtifactType artifactType = artifactTypeRepository.findByTypeId(typeId);
        Project project = artifactType.getProject();
        this.resourceBuilder.setProject(project).withEditProject();
        artifactTypeRepository.delete(artifactType);
        this.serviceProvider
            .getNotificationService()
            .broadcastChange(
                EntityChangeBuilder
                    .create(artifactType.getProject().getProjectId())
                    .withTypeDelete(artifactType.getTypeId())
                    .withUpdateLayout());
    }
}
