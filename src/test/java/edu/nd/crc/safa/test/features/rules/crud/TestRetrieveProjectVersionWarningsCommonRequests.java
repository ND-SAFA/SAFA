package edu.nd.crc.safa.test.features.rules.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.features.rules.TestRules;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Responsible for testing if you can retrieve the warnings
 * present in a specified project version.
 */
class TestRetrieveProjectVersionWarningsCommonRequests extends ApplicationBaseTest {

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

        TestRules.getDefaultRules().forEach(rule ->
            serviceProvider.getRuleService().addRule(projectVersion.getProject(), rule));

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
        this.rootBuilder
            .notifications(n -> n.
                initializeUser(getCurrentUser(), getToken(getCurrentUser()))
                .subscribeToVersion(getCurrentUser(), projectVersion));

        // Step - Create Design artifact and link
        JSONObject designJson =
            this.jsonBuilder
                .withProject(projectName, projectName, "")
                .withArtifactAndReturn(projectName,
                    null,
                    Design.name, Design.type,
                    null
                );
        JSONObject traceJson = this.jsonBuilder.withTraceAndReturn(projectName, Design.name, Requirement.name);
        CommitBuilder commitBuilder = CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(designJson)
            .withAddedTrace(traceJson);
        ProjectCommitDefinition addDesignCommit = commitService.commit(commitBuilder);

        // VP - Receive expected messages
        // TODO - fails due to intercepting a notification that's not meant for it
        /*EntityChangeMessage message = notificationService.getNextMessage(defaultUser);
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
        assertThat(warningsChange.getAction()).isEqualTo(Change.Action.UPDATE);*/

        // Step - Retrieve project warnings
        JSONObject rulesWithDesign = getProjectRules(projectVersion);

        // VP - Verify that no rules are generated
        assertThat(rulesWithDesign.length()).isZero();

        // Step - Delete design artifact
        ArtifactAppEntity updatedDesign = addDesignCommit.getArtifact(ModificationType.ADDED, 0);
        ProjectCommitDefinition deletionCommit = commitService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withRemovedArtifact(updatedDesign));

        // VP - Verify that trace was deleted too
        List<TraceAppEntity> deletedTraces = deletionCommit.getTraces().getRemoved();
        assertThat(deletedTraces).hasSize(1);

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
