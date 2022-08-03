package unit.project.rule;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.layout.RuleAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.utilities.JsonFileUtilities;
import edu.nd.crc.safa.warnings.RuleName;

import com.fasterxml.jackson.core.type.TypeReference;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

class TestCreateAndRetrieveRule extends ApplicationBaseTest {

    List<IRuleTest> ruleTests = List.of(new AtLeastOneRule());

    @Test
    void createAtLeastOneRule() throws Exception {

        for (IRuleTest ruleTest : ruleTests) {
            String projectName = ruleTest.getProjectName();
            ProjectVersion projectVersion = this.dbEntityBuilder
                .newProject(projectName)
                .newVersionWithReturn(projectName);
            Project project = projectVersion.getProject();

            // Step - Create rule
            RuleAppEntity rule = ruleTest.getRule();
            JSONObject ruleCreated = SafaRequest
                .withRoute(AppRoutes.Projects.Rules.CREATE_WARNING_IN_PROJECT)
                .withProject(project)
                .postWithJsonObject(rule);

            // VP - Verify that ID is returned
            assertThat(ruleCreated).isNotNull();
            assertObjectsMatch(JsonFileUtilities.toJson(rule), ruleCreated, List.of("id"));

            // Step - Create violating rule entities
            ruleTest.createViolatingRuleEntities(projectVersion, this.dbEntityBuilder);

            // Step - Retrieve project warnings
            JSONObject projectWarnings = SafaRequest
                .withRoute(AppRoutes.Projects.Rules.GET_WARNINGS_IN_PROJECT_VERSION)
                .withVersion(projectVersion)
                .getWithJsonObject();

            // Step - Parse warnings
            TypeReference<Map<String, List<RuleName>>> typeRef = new TypeReference<>() {
            };
            Map<String, List<RuleName>> warnings = JsonFileUtilities.parse(projectWarnings.toString(), typeRef);

            // Verify - Verify that warnings are as expected
            ruleTest.assertWarnings(warnings);
        }
    }
}
