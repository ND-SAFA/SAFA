package unit.project.rule;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.layout.RuleAppEntity;
import edu.nd.crc.safa.server.entities.api.layout.RuleCondition;
import edu.nd.crc.safa.server.entities.api.layout.RuleRelation;
import edu.nd.crc.safa.server.entities.db.Project;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

public class TestCreateAndRetrieveRule extends ApplicationBaseTest {


    @Test
    public void createDefaultRule() throws Exception {
        String projectName = "test";
        String ruleName = "test-rule";
        String ruleDescription = "test-description";
        String sourceType = "Requirements";
        String targetType = "Designs";

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

        // VP - Able to retrieve rule
    }
}
