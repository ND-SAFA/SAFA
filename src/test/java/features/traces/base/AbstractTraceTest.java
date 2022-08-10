package features.traces.base;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Optional;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;

import features.base.ApplicationBaseTest;

/**
 * Tests that generated trace links are reviewed.
 */
public abstract class AbstractTraceTest extends ApplicationBaseTest {

    protected void assertTraceExists(Project project, String sourceName, String targetName) {
        assertTraceStatus(project, sourceName, targetName, true);
    }

    protected void assertTraceDoesNotExist(Project project, String sourceName, String targetName) {
        assertTraceStatus(project, sourceName, targetName, false);
    }

    protected void assertTraceStatus(Project project, String sourceName, String targetName, boolean exists) {
        Optional<TraceLink> traceLinkQuery =
            this.traceLinkRepository.getByProjectAndSourceAndTarget(project,
                sourceName,
                targetName);
        assertThat(traceLinkQuery.isPresent()).isEqualTo(exists);
    }

    protected String getGeneratedLinkEndpoint(ProjectVersion projectVersion) {

        return RouteBuilder
            .withRoute(AppRoutes.Projects.Links.GET_GENERATED_LINKS_IN_PROJECT_VERSION)
            .withVersion(projectVersion)
            .buildEndpoint();
    }
}
