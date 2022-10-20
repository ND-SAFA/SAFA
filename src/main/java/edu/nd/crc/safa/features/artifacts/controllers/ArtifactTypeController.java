package edu.nd.crc.safa.features.artifacts.controllers;

import java.util.List;
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
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.ArtifactType;
import edu.nd.crc.safa.features.types.TypeAppEntity;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
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
     * Returns list of artifact types in project.
     *
     * @param projectId The id of the project whose types are returned.
     * @return List of artifact types.
     * @throws SafaError Throws error if user does not have viewing permission on project.
     */
    @GetMapping(AppRoutes.ArtifactType.GET_PROJECT_ARTIFACT_TYPES)
    public List<TypeAppEntity> getProjectArtifactTypes(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        return this.serviceProvider.getTypeService().getAppEntities(project);
    }

    /**
     * Creates or updates given artifact type entity on specified project.
     *
     * @param projectId    The id of the project whose type is created / updated for.
     * @param artifactType The artifact type to create or update.
     * @return The updated artifact type with id if being created.
     * @throws SafaError Throws error if user does not have edit permissions on project.
     */
    @PostMapping(AppRoutes.ArtifactType.CREATE_OR_UPDATE_ARTIFACT_TYPE)
    public TypeAppEntity createOrUpdateArtifactType(@PathVariable UUID projectId,
                                                    @RequestBody ArtifactType artifactType) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        artifactType.setProject(project);
        this.serviceProvider.getArtifactTypeRepository().save(artifactType);

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
                    .create(projectId)
                    .withTypeUpdate(artifactType.getTypeId())
                    .withArtifactsUpdate(artifactIds));
        return new TypeAppEntity(artifactType);
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
