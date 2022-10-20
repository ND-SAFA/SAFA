package edu.nd.crc.safa.features.models.tgen.controllers;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/**
 * Responsible for generating trace links between artifact types and
 * retrieving them.
 */
@RestController
public class GeneratedLinkController extends BaseController {

    @Autowired
    public GeneratedLinkController(ResourceBuilder resourceBuilder,
                                   ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Returns generated links in project version.
     *
     * @param versionId The UUID of project version to retrieve from.
     * @return List of trace app entities representing generated links in project version.
     * @throws SafaError If user does not have permissions to access this project.
     */
    @GetMapping(value = AppRoutes.Links.GET_GENERATED_LINKS_IN_PROJECT_VERSION)
    public List<TraceAppEntity> getGeneratedLinks(@PathVariable UUID versionId) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();
        return this.serviceProvider
            .getTraceService()
            .getAppEntities(projectVersion, (t) -> true)
            .stream()
            .filter(t -> t.getTraceType().equals(TraceType.GENERATED))
            .collect(Collectors.toList());
    }
}
