package edu.nd.crc.safa.features.generation.summary;

import java.util.List;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.builders.ProjectSummaryJobBuilder;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.config.SummarizationMaxProjectSizeCheck;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides summarization endpoints.
 */
@RestController
public class SummarizeController extends BaseController {
    public SummarizeController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Performs summary request.
     *
     * @param versionId The version of the artifact to summarize.
     * @param request   Defines content to summarize and model to do it with.
     * @return List of summaries.
     */
    @PostMapping(AppRoutes.Summarize.SUMMARIZE_ARTIFACTS)
    public List<ArtifactAppEntity> summarizeArtifacts(@PathVariable UUID versionId,
                                                      @RequestBody @Valid SummarizeArtifactRequestDTO request) {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getProjectVersion(versionId, user, request);
        request.setProjectVersion(projectVersion);
        request.setProjectSummary(projectVersion.getProject().getSpecification());
        return getServiceProvider().getSummaryService().generateArtifactSummaries(request);
    }

    @PostMapping(AppRoutes.Summarize.SUMMARIZE_PROJECT)
    public JobAppEntity summarizeProject(@PathVariable UUID versionId) throws Exception {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getProjectVersion(versionId, user, null);
        return new ProjectSummaryJobBuilder(user, this.getServiceProvider(), projectVersion).perform();
    }

    private ProjectVersion getProjectVersion(UUID versionId, SafaUser user, SummarizeArtifactRequestDTO request) {
        AdditionalPermissionCheck maxSizeCheck;
        if (request != null) {
            maxSizeCheck = new SummarizationMaxProjectSizeCheck(request);
        } else {
            maxSizeCheck = new SummarizationMaxProjectSizeCheck();
        }

        return getResourceBuilder()
            .fetchVersion(versionId)
            .asUser(user)
            .withPermissions(Set.of(ProjectPermission.GENERATE, ProjectPermission.EDIT_DATA))
            .withAdditionalCheck(maxSizeCheck)
            .get();
    }
}
