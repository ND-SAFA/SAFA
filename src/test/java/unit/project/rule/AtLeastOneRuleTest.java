package unit.project.rule;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.builders.entities.DbEntityBuilder;
import edu.nd.crc.safa.server.entities.api.layout.RuleAppEntity;
import edu.nd.crc.safa.server.entities.api.layout.RuleCondition;
import edu.nd.crc.safa.server.entities.api.layout.RuleRelation;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.warnings.RuleName;

public class AtLeastOneRuleTest implements IRuleTest {
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
        assertThat(warnings.containsKey(artifactId)).isTrue();
        String violatedRuleName = warnings
            .get(artifactId)
            .get(0)
            .ruleName;
        assertThat(violatedRuleName).isEqualTo(ruleName);
    }
}
