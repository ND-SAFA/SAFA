package unit.warnings;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;
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
            .newTraceLink(projectName, sourceName, targetName);

        ProjectVersion projectVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        List<ArtifactBody> projectBodies = dbEntityBuilder.getArtifactBodies(projectName);
        List<TraceLink> traceLinks = dbEntityBuilder.getTraceLinks(projectName);
        Map<String, List<RuleName>> violations = warningService.findViolationsInArtifactTree(projectVersion,
            projectBodies,
            traceLinks);

        assertThat(violations.containsKey(targetName)).isTrue();
    }
}
