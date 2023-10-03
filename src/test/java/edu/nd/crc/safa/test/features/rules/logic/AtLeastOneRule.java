package edu.nd.crc.safa.test.features.rules.logic;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.rules.entities.app.RuleAppEntity;
import edu.nd.crc.safa.features.rules.entities.app.RuleCondition;
import edu.nd.crc.safa.features.rules.entities.app.RuleRelation;
import edu.nd.crc.safa.features.rules.parser.RuleName;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.services.builders.DbEntityBuilder;

/**
 * Defines a rule test consisting of creating a rule constraining
 * defined source type to have at least one child of a defined target
 * type.
 */
public class AtLeastOneRule implements IRuleTest {
    String projectName = "test";
    String ruleName = "test-rule";
    String ruleDescription = "test-description";
    String sourceType = "MadeUpSource";
    String targetType = "MadeUpTarget";
    String artifactName = "RE-20";
    ArtifactVersion artifactVersion = null;

    @Override
    public RuleAppEntity getRule() {
        return new RuleAppEntity(
            null,
            ruleName,
            ruleDescription,
            RuleCondition.AT_LEAST_N,
            1,
            sourceType,
            RuleRelation.CHILD,
            targetType,
            new ArrayList<>()
        );
    }

    @Override
    public String getProjectName() {
        return projectName;
    }

    @Override
    public void createViolatingRuleEntities(ProjectVersion projectVersion,
                                            DbEntityBuilder entityBuilder) {
        this.artifactVersion = entityBuilder
            .newType(projectName, sourceType)
            .newArtifactAndBody(projectName, sourceType, artifactName, "", "")
            .getArtifactBody(projectName, artifactName, 0);
    }

    @Override
    public void assertWarnings(Map<String, List<RuleName>> warnings) {
        String artifactId = artifactVersion.getArtifact().getArtifactId().toString();
        assertThat(artifactId).isNotNull();
        assertThat(warnings).containsKey(artifactId);
        String violatedRuleName = warnings
            .get(artifactId)
            .get(0)
            .getRuleName();
        assertThat(violatedRuleName).isEqualTo(ruleName);
    }
}
