package unit.warnings;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Hashtable;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.common.AppRoutes;
import edu.nd.crc.safa.server.entities.app.project.VersionEntityTypes;
import edu.nd.crc.safa.server.entities.app.project.VersionMessage;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Responsible for testing if you can retrieve the warnings
 * present in a specified project version.
 */
public class TestRetrieveProjectVersionWarnings extends ApplicationBaseTest {

    /**
     * Uses atLeastOneRequirementOrDesignOrProcessForRequirement default rule to expect
     * 1. No warning retrieved on an empty project
     * 2. Single warning retrieved when a sole requirement exists
     * 3. No warning exists with a second design artifact is connecte to requirement
     */
    @Test
    public void testRetrievingProjectWarnings() throws Exception {
        String projectName = "project-name";
        String requirementName = "RE-20";
        String requirementType = "Requirement";
        String designName = "DD-10";
        String designType = "Design";

        // Step - Create project, version, and requirement + design artifacts.
        ProjectVersion projectVersion = this.dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        // Step - Retrieve project warnings
        JSONObject emptyRules = getProjectRules(projectVersion);

        // VP - Verify that no rules are retrieved
        assertThat(emptyRules.length()).isEqualTo(0);

        // Step - Create requirement artifact
        String requirementId = this.dbEntityBuilder
            .newType(projectName, requirementType)
            .newArtifactAndBody(projectName, requirementType, requirementName, "", "")
            .getArtifact(projectName, requirementName)
            .getArtifactId().toString();

        // Step - Retrieve project warnings
        JSONObject warningsWithRequirement = getProjectRules(projectVersion);

        // VP - Verify that `missing child` warning is retrieved
        assertThat(warningsWithRequirement.length()).isEqualTo(1);
        JSONArray rulesViolated = warningsWithRequirement.getJSONArray(requirementId);
        assertThat(rulesViolated.length()).isEqualTo(1);
        JSONObject ruleViolated = rulesViolated.getJSONObject(0);
        assertThat(ruleViolated.getString("ruleName")).isEqualTo("Missing child");

        // Step - Subscribe to project version
        createNewConnection(currentUsername)
            .subscribeToVersion(currentUsername, projectVersion);

        // Step - Create Design artifact and link
        JSONObject designJson =
            this.jsonBuilder
                .withProject(projectName, projectName, "")
                .withArtifactAndReturn(projectName,
                    "",
                    designName, designType,
                    ""
                );
        JSONObject traceJson = this.jsonBuilder.withTraceAndReturn(projectName, designName, requirementName);
        CommitBuilder commitBuilder = CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(designJson)
            .withAddedTrace(traceJson);
        designJson = commit(commitBuilder);

        // VP - Receive expected messages
        Hashtable<VersionEntityTypes, VersionMessage> messages = new Hashtable<>();
        int nExpectedMessages = getQueueSize(currentUsername);
        for (int i = 0; i < nExpectedMessages; i++) {
            VersionMessage message = getNextMessage(currentUsername, VersionMessage.class);
            messages.put(message.getType(), message);
        }
        assertThat(messages.containsKey(VersionEntityTypes.ARTIFACTS)).isTrue();
        assertThat(messages.containsKey(VersionEntityTypes.TRACES)).isTrue();
        assertThat(messages.containsKey(VersionEntityTypes.WARNINGS)).isTrue();

        // Step - Retrieve project warnings
        JSONObject rulesWithDesign = getProjectRules(projectVersion);

        // VP - Verify that no rules are generated
        assertThat(rulesWithDesign.length()).isEqualTo(0);

        // Step - Delete design artifact
        JSONObject updatedDesign = designJson
            .getJSONObject("artifacts")
            .getJSONArray("added")
            .getJSONObject(0);
        JSONObject deletionCommit =
            commit(CommitBuilder.withVersion(projectVersion).withRemovedArtifact(updatedDesign));

        // VP - Verify that trace was deleted too
        JSONArray deletedTraces = deletionCommit.getJSONObject("traces").getJSONArray("removed");
        assertThat(deletedTraces.length()).isEqualTo(1);

        // Step - Retrieve project warnings
        JSONObject rulesAfterDelete = getProjectRules(projectVersion);

        // VP - Verify that rule is generated against
        assertThat(rulesAfterDelete.length()).isEqualTo(1);
        JSONObject ruleViolatedAfterDelete = rulesViolated.getJSONObject(0);
        assertThat(ruleViolatedAfterDelete.getString("ruleName")).isEqualTo("Missing child");
    }

    private JSONObject getProjectRules(ProjectVersion projectVersion) throws Exception {
        String endpoint = RouteBuilder
            .withRoute(AppRoutes.Projects.Warnings.getWarningsInProjectVersion)
            .withVersion(projectVersion)
            .get();
        return sendGet(endpoint, status().is2xxSuccessful());
    }
}
