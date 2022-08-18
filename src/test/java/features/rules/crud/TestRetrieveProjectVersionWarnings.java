package features.rules.crud;

import static org.assertj.core.api.Assertions.assertThat;

import builders.CommitBuilder;
import requests.SafaRequest;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import features.base.ApplicationBaseTest;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Responsible for testing if you can retrieve the warnings
 * present in a specified project version.
 */
class TestRetrieveProjectVersionWarnings extends ApplicationBaseTest {

    /**
     * Uses atLeastOneRequirementOrDesignOrProcessForRequirement default rule to expect
     * 1. No warning retrieved on an empty project
     * 2. Single warning retrieved when a sole requirement exists
     * 3. No warning exists with a second design artifact is connected to requirement
     */
    @Test
    void testRetrievingProjectWarnings() throws Exception {

        // Step - Create project, version, and requirement + design artifacts.
        ProjectVersion projectVersion = this.dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        // Step - Retrieve project warnings
        JSONObject emptyRules = getProjectRules(projectVersion);

        // VP - Verify that no rules are retrieved
        assertThat(emptyRules.length()).isZero();

        // Step - Create requirement artifact
        String requirementId = this.dbEntityBuilder
            .newType(projectName, Requirement.type)
            .newArtifactAndBody(projectName, Requirement.type, Requirement.name, "", "")
            .getArtifact(projectName, Requirement.name)
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
        notificationTestService.createNewConnection(defaultUser).subscribeToVersion(defaultUser, projectVersion);

        // Step - Create Design artifact and link
        JSONObject designJson =
            this.jsonBuilder
                .withProject(projectName, projectName, "")
                .withArtifactAndReturn(projectName,
                    "",
                    Design.name, Design.type,
                    ""
                );
        JSONObject traceJson = this.jsonBuilder.withTraceAndReturn(projectName, Design.name, Requirement.name);
        CommitBuilder commitBuilder = CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(designJson)
            .withAddedTrace(traceJson);
        designJson = commitTestService.commit(commitBuilder);

        // VP - Receive expected messages
        EntityChangeMessage message = notificationTestService.getNextMessage(defaultUser);
        assertThat(message.getChanges()).hasSize(3);
        assertThat(message.getChangedEntities())
            .contains(Change.Entity.ARTIFACTS)
            .contains(Change.Entity.TRACES)
            .contains(Change.Entity.WARNINGS);

        // VP - Verify artifact change
        Change artifactChange = message.getChangeForEntity(Change.Entity.ARTIFACTS);
        assertThat(artifactChange.getAction()).isEqualTo(Change.Action.UPDATE);

        // VP - Verify trace change
        Change traceChange = message.getChangeForEntity(Change.Entity.TRACES);
        assertThat(traceChange.getAction()).isEqualTo(Change.Action.UPDATE);

        // VP - Verify warning change
        Change warningsChange = message.getChangeForEntity(Change.Entity.WARNINGS);
        assertThat(warningsChange.getAction()).isEqualTo(Change.Action.UPDATE);

        // Step - Retrieve project warnings
        JSONObject rulesWithDesign = getProjectRules(projectVersion);

        // VP - Verify that no rules are generated
        assertThat(rulesWithDesign.length()).isZero();

        // Step - Delete design artifact
        JSONObject updatedDesign = designJson
            .getJSONObject("artifacts")
            .getJSONArray("added")
            .getJSONObject(0);
        JSONObject deletionCommit =
            commitTestService.commit(CommitBuilder.withVersion(projectVersion).withRemovedArtifact(updatedDesign));

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
        return new SafaRequest(AppRoutes.Rules.GET_WARNINGS_IN_PROJECT_VERSION)
            .withVersion(projectVersion)
            .getWithJsonObject();
    }

    static class Requirement {
        public static final String name = "RE-20";
        public static final String type = "Requirement";
    }

    static class Design {
        public static final String name = "DD-10";
        public static final String type = "Design";
    }
}
