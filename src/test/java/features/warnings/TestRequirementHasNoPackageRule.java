package unit.warnings;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.rules.services.RuleService;
import edu.nd.crc.safa.features.rules.parser.RuleName;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

class TestRequirementHasNoPackageRule extends ApplicationBaseTest {

    @Autowired
    RuleService ruleService;

    @Test
    void testRequirementHasNoPackageLink() {
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

        Project project = dbEntityBuilder.getProject(projectName);
        List<ArtifactVersion> projectBodies = dbEntityBuilder.getArtifactBodies(projectName);
        List<TraceLinkVersion> traceLinkVersions = dbEntityBuilder.getTraceLinks(projectName);
        List<TraceLink> traceLinks = traceLinkVersions
            .stream()
            .map(TraceLinkVersion::getTraceLink)
            .collect(Collectors.toList());
        Map<String, List<RuleName>> violations = ruleService.generateWarningsOnEntities(project,
            projectBodies,
            traceLinks);

        // VP - Verify that target triggered warning
        String targetId = this.dbEntityBuilder.getArtifact(projectName, targetName).getArtifactId().toString();
        assertThat(violations).containsKey(targetId);
    }
}
