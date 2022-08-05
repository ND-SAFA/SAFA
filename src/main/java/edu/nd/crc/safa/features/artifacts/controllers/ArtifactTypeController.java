package edu.nd.crc.safa.features.artifacts.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactType;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.notifications.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.ProjectEntityTypes;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;

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

    ArtifactTypeRepository artifactTypeRepository;
    NotificationService notificationService;

    @Autowired
    public ArtifactTypeController(ResourceBuilder resourceBuilder,
                                  ArtifactTypeRepository artifactTypeRepository,
                                  NotificationService notificationService) {
        super(resourceBuilder);
        this.artifactTypeRepository = artifactTypeRepository;
        this.notificationService = notificationService;
    }

    /**
     * Returns list of artifact types in project.
     *
     * @param projectId The id of the project whose types are returned.
     * @return List of artifact types.
     * @throws SafaError Throws error if user does not have viewing permission on project.
     */
    @GetMapping(AppRoutes.Projects.ArtifactType.GET_PROJECT_ARTIFACT_TYPES)
    public List<ArtifactType> getProjectArtifactTypes(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        return this.artifactTypeRepository.findByProject(project);
    }

    /**
     * Creates or updates given artifact type entity on specified project.
     *
     * @param projectId    The id of the project whose type is created / updated for.
     * @param artifactType The artifact type to create or update.
     * @return The updated artifact type with id if being created.
     * @throws SafaError Throws error if user does not have edit permissions on project.
     */
    @PostMapping(AppRoutes.Projects.ArtifactType.CREATE_OR_UPDATE_ARTIFACT_TYPE)
    public ArtifactType createOrUpdateArtifactType(@PathVariable UUID projectId,
                                                   @RequestBody ArtifactType artifactType) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        artifactType.setProject(project);
        this.artifactTypeRepository.save(artifactType);
        this.notificationService.broadUpdateProjectMessage(project, ProjectEntityTypes.TYPES);
        return artifactType;
    }

    /**
     * Deletes the artifact type with specified type id.
     *
     * @param typeId The id of the type to delete.
     * @throws SafaError Throws error if user does not have edit permissions on project.
     */
    @DeleteMapping(AppRoutes.Projects.ArtifactType.DELETE_ARTIFACT_TYPE)
    public void deleteArtifactType(@PathVariable UUID typeId) throws SafaError {
        ArtifactType artifactType = this.artifactTypeRepository.findByTypeId(typeId);
        Project project = artifactType.getProject();
        this.resourceBuilder.setProject(project).withEditProject();
        this.artifactTypeRepository.delete(artifactType);
        this.notificationService.broadUpdateProjectMessage(project, ProjectEntityTypes.TYPES);
    }
}
