package unit.project.links;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.Optional;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;

import unit.ApplicationBaseTest;

/**
 * Tests that generated trace links are able to be reviewed.
 */
public class TraceBaseTest extends ApplicationBaseTest {

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
            .withRoute(AppRoutes.Projects.getGeneratedLinksInProjectVersion)
            .withVersion(projectVersion)
            .get();
    }
}
