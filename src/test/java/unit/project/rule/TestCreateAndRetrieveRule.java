package unit.project.rule;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.layout.RuleAppEntity;
import edu.nd.crc.safa.server.entities.api.layout.RuleCondition;
import edu.nd.crc.safa.server.entities.api.layout.RuleRelation;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

public class TestCreateAndRetrieveRule extends ApplicationBaseTest {


    @Test
    public void createAtLeastOneRule() throws Exception {
        String projectName = "test";
        String ruleName = "test-rule";
        String ruleDescription = "test-description";
        String sourceType = "MadeUpSource";
        String targetType = "MadeUpTarget";

        Project project = this.dbEntityBuilder.newProjectWithReturn(projectName);
        String route =
            RouteBuilder
                .withRoute(AppRoutes.Projects.Rules.createWarningInProject)
                .withProject(project)
                .get();

        RuleAppEntity rule = new RuleAppEntity(
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
        JSONObject ruleCreated = sendPost(route, toJson(rule));

        // VP - Id is attached
        assertThat(ruleCreated).isNotNull();
        assertObjectsMatch(toJson(rule), ruleCreated, List.of("id"));

        // Step - Create version and violating artifact
        String artifactName = "RE-20";
        ProjectVersion projectVersion = this.dbEntityBuilder
            .newVersion(projectName)
            .newType(projectName, sourceType)
            .newArtifactAndBody(projectName, sourceType, artifactName, "", "")
            .getProjectVersion(projectName, 0);
        ArtifactVersion artifactVersion = this.dbEntityBuilder.getArtifactBody(projectName, artifactName, 0);

        // Step - Retrieve project warning
        String getProjectWarningEndpoint =
            RouteBuilder
                .withRoute(AppRoutes.Projects.Rules.getWarningsInProjectVersion)
                .withVersion(projectVersion).get();
        JSONObject projectWarnings = sendGet(getProjectWarningEndpoint);

        // VP - Assert that warnings are generated
        String artifactId = artifactVersion.getArtifact().getArtifactId().toString();
        assertThat(artifactId).isNotNull();
        assertThat(projectWarnings.has(artifactId)).isTrue();
        String violatedRuleName = projectWarnings.getJSONObject(artifactId).getString("name");
        assertThat(violatedRuleName).isEqualTo(ruleName);
    }
}
