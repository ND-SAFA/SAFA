package unit.warnings;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.warnings.ArtifactRelationship;
import edu.nd.crc.safa.warnings.Condition;
import edu.nd.crc.safa.warnings.DefaultTreeRules;
import edu.nd.crc.safa.warnings.Function;
import edu.nd.crc.safa.warnings.RuleName;
import edu.nd.crc.safa.warnings.TreeVerifier;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Provides a smoke test for various types of rules that are used
 * to generated project warnings.
 */
public class SmokeTests extends ApplicationBaseTest {

    @Test
    public void testLinkNodesFunction() {
        String sourceName = "EntityPackage";
        String targetName = "RE-8";
        TreeVerifier verifier = new TreeVerifier();

        Function function = new Function();
        function.artifactRelationship = ArtifactRelationship.BIDIRECTIONAL_LINK;
        function.targetArtifactType = "Requirement";
        function.sourceArtifactType = "Package";
        function.condition = Condition.EXACTLY;
        function.count = 0;

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
    public void testChildFunction() {
        String sourceName = "EntityPackage";
        String targetName = "RE-8";
        TreeVerifier verifier = new TreeVerifier();

        Function function = new Function();
        function.artifactRelationship = ArtifactRelationship.CHILD;
        function.targetArtifactType = "Requirement";
        function.sourceArtifactType = "Package";
        function.condition = Condition.EXACTLY;
        function.count = 0;

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
    public void testFindRuleViolations() {
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

        List<ArtifactVersion> projectBodies = dbEntityBuilder.getArtifactBodies(projectName);
        List<TraceLinkVersion> traceLinkVersions = dbEntityBuilder.getTraceLinks(projectName);
        List<TraceLink> traceLinks =
            traceLinkVersions.stream().map(TraceLinkVersion::getTraceLink).collect(Collectors.toList());
        TreeVerifier verifier = new TreeVerifier();
        Map<String, List<RuleName>> violatedRules = verifier.findRuleViolations(projectBodies, traceLinks,
            DefaultTreeRules.getDefaultRules());

        assertThat(violatedRules.size()).isEqualTo(1);

        assertThat(violatedRules.get(targetName).size()).isEqualTo(2);
        String targetRule = violatedRules.get(targetName).get(0).toString();
        assertThat(targetRule).contains("design or process");
        targetRule = violatedRules.get(targetName).get(1).toString();
        assertThat(targetRule).contains("must not have package children");

    }
}
