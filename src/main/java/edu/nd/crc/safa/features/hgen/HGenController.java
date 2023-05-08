package edu.nd.crc.safa.features.hgen;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for creating parent artifacts.
 */
@RestController
public class HGenController extends BaseController {
    public HGenController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Generates hierarchy above artifacts in request.
     *
     * @param request Contains artifacts and clusters within them.
     * @return List of generates artifacts for new level.
     */
    @PostMapping(AppRoutes.HGen.GENERATE)
    public List<String> generateHierarchy(@PathVariable UUID versionId, @RequestBody HGenRequestDTO request) {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();
        return this.serviceProvider.getHGenService().generateHierarchy(projectVersion, request);
    }
}
