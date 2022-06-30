package unit.project.rule;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.layout.RuleAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.warnings.RuleName;

import com.fasterxml.jackson.core.type.TypeReference;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

public class TestCreateAndRetrieveRule extends ApplicationBaseTest {

    List<IRuleTest> ruleTests = List.of(new AtLeastOneRuleTest());

    @Test
    public void createAtLeastOneRule() throws Exception {

        for (IRuleTest ruleTest : ruleTests) {
            String projectName = ruleTest.getProjectName();
            ProjectVersion projectVersion = this.dbEntityBuilder
                .newProject(projectName)
                .newVersionWithReturn(projectName);
            Project project = projectVersion.getProject();

            // Step - Create rule
            String route =
                RouteBuilder
                    .withRoute(AppRoutes.Projects.Rules.createWarningInProject)
                    .withProject(project)
                    .get();
            RuleAppEntity rule = ruleTest.getRule();
            JSONObject ruleCreated = sendPost(route, toJson(rule));

            // VP - Verify that ID is returned
            assertThat(ruleCreated).isNotNull();
            assertObjectsMatch(toJson(rule), ruleCreated, List.of("id"));

            // Step - Create violating rule entities
            ruleTest.createViolatingRuleEntities(projectVersion, this.dbEntityBuilder);

            // Step - Retrieve project warnings
            String getProjectWarningEndpoint =
                RouteBuilder
                    .withRoute(AppRoutes.Projects.Rules.getWarningsInProjectVersion)
                    .withVersion(projectVersion).get();
            JSONObject projectWarnings = sendGet(getProjectWarningEndpoint);

            // Step - Parse warnings
            TypeReference<Map<String, List<RuleName>>> typeRef = new TypeReference<>() {
            };
            Map<String, List<RuleName>> warnings = getMapper().readValue(projectWarnings.toString(), typeRef);

            // Verify - Verify that warnings are as expected
            ruleTest.assertWarnings(warnings);
        }
    }
}
