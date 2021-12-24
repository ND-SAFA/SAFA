package unit.warnings;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.server.services.WarningService;
import edu.nd.crc.safa.warnings.RuleName;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

public class TestRequirementHasNoPackageRule extends ApplicationBaseTest {

    @Autowired
    WarningService warningService;

    @Test
    public void testRequirementHasNoPackageLink() {
        String projectName = "test-project";
        String targetType = "Requirement";
        String targetName = "RE-8";
        String sourceType = "Package";
        String sourceName = "entities";

        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, targetType)
            .newArtifact(projectName, targetType, targetName)
            .newArtifactBody(projectName, targetName, "", "")
            .newType(projectName, sourceType)
            .newArtifact(projectName, sourceType, sourceName)
            .newArtifactBody(projectName, sourceName, "", "")
            .newTraceLink(projectName, sourceName, targetName, 0);

        ProjectVersion projectVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        List<ArtifactVersion> projectBodies = dbEntityBuilder.getArtifactBodies(projectName);
        List<TraceLinkVersion> traceLinkVersions = dbEntityBuilder.getTraceLinks(projectName);
        List<TraceLink> traceLinks = traceLinkVersions.stream().map(TraceLinkVersion::getTraceLink).collect(Collectors.toList());
        Map<String, List<RuleName>> violations = warningService.findViolationsInArtifactTree(projectVersion,
            projectBodies,
            traceLinks);

        // VP - Verify that target triggered warning
        String targetId = this.dbEntityBuilder.getArtifact(projectName, targetName).getArtifactId().toString();
        assertThat(violations.containsKey(targetId)).isTrue();
    }
}
