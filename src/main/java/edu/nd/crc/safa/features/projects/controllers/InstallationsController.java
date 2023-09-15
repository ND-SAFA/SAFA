package edu.nd.crc.safa.features.projects.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.installations.InstallationDTO;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints to retrieve installations and projects that imported them
 */
@RestController
public class InstallationsController extends BaseController {

    private final ProjectRepository projectRepository;

    @Autowired
    public InstallationsController(ResourceBuilder resourceBuilder,
                                   ServiceProvider serviceProvider,
                                   ProjectRepository projectRepository) {
        super(resourceBuilder, serviceProvider);
        this.projectRepository = projectRepository;
    }

    @GetMapping(AppRoutes.Projects.Installations.BY_PROJECT)
    @Operation(
        method = "GET",
        summary = "Find all installations for a certain SAFA project",
        responses = @ApiResponse(
            responseCode = "200",
            description = "A list with all installations imported by the specified project. "
                + "If the project does not exist the result is empty",
            useReturnTypeSchema = true
        )
    )
    public List<InstallationDTO> getInstallationsByProject(@PathVariable("id") UUID id) {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        getResourceBuilder().fetchProject(id).withPermission(ProjectPermission.VIEW, user);
        return this.projectRepository.findInstallationsByProjectId(id);
    }

}
