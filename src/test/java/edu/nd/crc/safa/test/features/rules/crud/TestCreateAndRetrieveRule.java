package edu.nd.crc.safa.test.features.rules.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.rules.entities.app.RuleAppEntity;
import edu.nd.crc.safa.features.rules.parser.RuleName;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.features.rules.logic.AtLeastOneRule;
import edu.nd.crc.safa.test.features.rules.logic.IRuleTest;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import com.fasterxml.jackson.core.type.TypeReference;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

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
                .withRoute(AppRoutes.Rules.CREATE_WARNING_IN_PROJECT)
                .withProject(project)
                .postWithJsonObject(rule);

            // VP - Verify that ID is returned
            assertThat(ruleCreated).isNotNull();
            assertionService.assertObjectsMatch(JsonFileUtilities.toJson(rule), ruleCreated, List.of("id"));

            // Step - Create violating rule entities
            ruleTest.createViolatingRuleEntities(projectVersion, this.dbEntityBuilder);

            // Step - Retrieve project warnings
            JSONObject projectWarnings = SafaRequest
                .withRoute(AppRoutes.Rules.GET_WARNINGS_IN_PROJECT_VERSION)
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
