package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ProjectEntityTypes;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactTypeRepository;
import edu.nd.crc.safa.server.services.NotificationService;

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
    @GetMapping(AppRoutes.Projects.ArtifactType.getProjectArtifactTypes)
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
    @PostMapping(AppRoutes.Projects.ArtifactType.createOrUpdateArtifactType)
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
    @DeleteMapping(AppRoutes.Projects.ArtifactType.deleteArtifactType)
    public void deleteArtifactType(@PathVariable UUID typeId) throws SafaError {
        ArtifactType artifactType = this.artifactTypeRepository.findByTypeId(typeId);
        Project project = artifactType.getProject();
        this.resourceBuilder.setProject(project).withEditProject();
        this.artifactTypeRepository.delete(artifactType);
        this.notificationService.broadUpdateProjectMessage(project, ProjectEntityTypes.TYPES);
    }
}
