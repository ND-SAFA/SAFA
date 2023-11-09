package edu.nd.crc.safa.features.types.controllers;

import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.TypeAppEntity;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.types.services.TypeService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

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

        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        Project project = getResourceBuilder().fetchProject(projectId)
                .withPermission(ProjectPermission.EDIT_DATA, user).get();
        TypeService typeService = getServiceProvider().getTypeService();
        artifactType = typeService.createArtifactType(project, artifactType.getName(), artifactType.getColor(), user);
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
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        Project project = getResourceBuilder().fetchProject(projectId)
                .withPermission(ProjectPermission.EDIT_DATA, user).get();
        TypeService typeService = getServiceProvider().getTypeService();
        artifactTypeObj = typeService.updateArtifactType(project, artifactTypeObj, user);
        return new TypeAppEntity(artifactTypeObj);
    }

    /**
     * Deletes the artifact type with specified type id.
     *
     * @param typeId The id of the type to delete.
     * @throws SafaError Throws error if user does not have edit permissions on project.
     */
    @DeleteMapping(AppRoutes.ArtifactType.DELETE_ARTIFACT_TYPE)
    public void deleteArtifactType(@PathVariable UUID typeId) throws SafaError {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();

        ArtifactType type = getResourceBuilder().fetchType(typeId)
            .withPermission(ProjectPermission.EDIT_DATA, user).get();

        getServiceProvider().getTypeService().deleteArtifactType(type, user);
    }
}
