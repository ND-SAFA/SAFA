package features.rules.logic;


import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactType;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.rules.parser.ArtifactRelationship;
import edu.nd.crc.safa.features.rules.parser.Condition;
import edu.nd.crc.safa.features.rules.parser.DefaultTreeRules;
import edu.nd.crc.safa.features.rules.parser.Function;
import edu.nd.crc.safa.features.rules.parser.RuleName;
import edu.nd.crc.safa.features.rules.parser.TreeVerifier;

import org.junit.jupiter.api.Test;
import features.base.ApplicationBaseTest;

/**
 * Provides a smoke test for various types of rules that are used
 * to generated project warnings.
 */
class SmokeTests extends ApplicationBaseTest {

    @Test
    void testLinkNodesFunction() {
        String sourceName = "EntityPackage";
        String targetName = "RE-8";
        TreeVerifier verifier = new TreeVerifier();

        Function function = new Function();
        function.setArtifactRelationship(ArtifactRelationship.BIDIRECTIONAL_LINK);
        function.setTargetArtifactType("Requirement");
        function.setSourceArtifactType("Package");
        function.setCondition(Condition.EXACTLY);
        function.setCount(0);

        ArtifactType sourceType = new ArtifactType();
        sourceType.setName("package");
        Artifact sourceArtifact = new Artifact();
        sourceArtifact.setName(sourceName);
        sourceArtifact.setType(sourceType);

        ArtifactType targetType = new ArtifactType();
        targetType.setName("requirement");
        Artifact targetArtifact = new Artifact();
        targetArtifact.setName(targetName);
        targetArtifact.setType(targetType);

        TraceLink link = new TraceLink(sourceArtifact, targetArtifact);

        List<TraceLink> links = new ArrayList<>();
        links.add(link);

        boolean result = verifier.satisfiesLinkCountRule(function, sourceArtifact, links);
        assertThat(result).isFalse();
        result = verifier.satisfiesLinkCountRule(function, targetArtifact, links);
        assertThat(result).isFalse();
    }

    @Test
    void testChildFunction() {
        String sourceName = "EntityPackage";
        String targetName = "RE-8";
        TreeVerifier verifier = new TreeVerifier();

        Function function = new Function();
        function.setArtifactRelationship(ArtifactRelationship.CHILD);
        function.setTargetArtifactType("Requirement");
        function.setSourceArtifactType("Package");
        function.setCondition(Condition.EXACTLY);
        function.setCount(0);

        ArtifactType sourceType = new ArtifactType();
        sourceType.setName("package");
        Artifact sourceArtifact = new Artifact();
        sourceArtifact.setName(sourceName);
        sourceArtifact.setType(sourceType);

        ArtifactType targetType = new ArtifactType();
        targetType.setName("requirement");
        Artifact targetArtifact = new Artifact();
        targetArtifact.setName(targetName);
        targetArtifact.setType(targetType);

        TraceLink link = new TraceLink(sourceArtifact, targetArtifact);

        List<TraceLink> links = new ArrayList<>();
        links.add(link);

        boolean isSatisfied = verifier.satisfiesChildCountRule(function, sourceName, links);
        assertThat(isSatisfied).isTrue();
        isSatisfied = verifier.satisfiesChildCountRule(function, targetName, links);
        assertThat(isSatisfied).isFalse();
    }

    @Test
    void testFindRuleViolations() {
        String projectName = "test-project";
        String sourceType = "Package";
        String targetType = "Requirement";
        String sourceName = "SomeClass.java";
        String targetName = "RE-8";

        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, sourceType)
            .newType(projectName, targetType)
            .newArtifact(projectName, sourceType, sourceName)
            .newArtifact(projectName, targetType, targetName)
            .newArtifactBody(projectName, sourceName, "", "")
            .newArtifactBody(projectName, targetName, "", "")
            .newTraceLink(projectName, sourceName, targetName, 0)
            .getProjectVersion(projectName, 0);

        List<ArtifactVersion> projectBodies = dbEntityBuilder.getArtifactBodies(projectName);
        List<TraceLink> traceLinks = this.traceLinkVersionRepository
            .getApprovedLinksInVersion(projectVersion)
            .stream()
            .map(TraceLinkVersion::getTraceLink)
            .collect(Collectors.toList());

        // Step - Calculate violated rules.
        TreeVerifier verifier = new TreeVerifier();
        Map<String, List<RuleName>> violatedRules = verifier.findRuleViolations(projectBodies, traceLinks,
            DefaultTreeRules.getDefaultRules());

        // VP - Verify that right warnings were triggered.
        String targetId = dbEntityBuilder.getArtifact(projectName, targetName).getArtifactId().toString();
        assertThat(violatedRules).hasSize(1);
        assertThat(violatedRules.get(targetId).size()).isEqualTo(2);
        String targetRule = violatedRules.get(targetId).get(0).toString();
        assertThat(targetRule).contains("design").contains("process");
        targetRule = violatedRules.get(targetId).get(1).toString();
        assertThat(targetRule).contains("must not have package children");
    }
}
