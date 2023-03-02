package edu.nd.crc.safa.test.features.rules.logic;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.rules.parser.RuleName;
import edu.nd.crc.safa.features.rules.services.RuleService;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.features.rules.TestRules;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

class TestRequirementHasNoPackageRule extends ApplicationBaseTest {

    @Autowired
    RuleService ruleService;

    @Test
    void testRequirementHasNoPackageLink() {
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
        TestRules.getDefaultRules().forEach(rule ->
            serviceProvider.getRuleService().addRule(project, rule));
        List<ArtifactVersion> projectBodies = dbEntityBuilder.getArtifactBodies(projectName);
        List<TraceLinkVersion> traceLinkVersions = dbEntityBuilder.getTraceLinks(projectName);
        List<TraceLink> traceLinks = traceLinkVersions
            .stream()
            .map(TraceLinkVersion::getTraceLink)
            .collect(Collectors.toList());
        Map<UUID, List<RuleName>> violations = ruleService.generateWarningsOnEntities(project,
            projectBodies,
            traceLinks);

        // VP - Verify that target triggered warning
        UUID targetId = this.dbEntityBuilder.getArtifact(projectName, targetName).getArtifactId();
        assertThat(violations).containsKey(targetId);
    }
}
