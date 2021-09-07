package unit.service;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.services.WarningService;
import edu.nd.crc.safa.warnings.RuleName;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.EntityBaseTest;

public class TestWarningService extends EntityBaseTest {

    @Autowired
    WarningService warningService;

    @Test
    public void testRequirementHasNoPackageLink() {
        String projectName = "test-project";
        String targetType = "Requirement";
        String targetName = "RE-8";
        String sourceType = "Package";
        String sourceName = "entities";

        entityBuilder
            .newProject(projectName)
            .newVersion(projectName)

            .newType(projectName, targetType)
            .newArtifact(projectName, targetType, targetName)
            .newArtifactBody(projectName, targetName, "", "")

            .newType(projectName, sourceType)
            .newArtifact(projectName, sourceType, sourceName)
            .newArtifactBody(projectName, sourceName, "", "")

            .newTraceLink(projectName, sourceName, targetName);

        Project project = entityBuilder.getProject(projectName);
        List<ArtifactBody> projectBodies = entityBuilder.getArtifactBodies(projectName);
        List<TraceLink> traceLinks = entityBuilder.getTraceLinks(projectName);
        Map<String, List<RuleName>> violations = warningService.findViolationsInArtifactTree(project, projectBodies,
            traceLinks);

        assertThat(violations.containsKey(targetName)).isTrue();
    }
}
