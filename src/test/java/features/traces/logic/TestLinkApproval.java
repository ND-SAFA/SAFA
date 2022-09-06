package features.traces.logic;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import builders.CommitBuilder;
import features.traces.base.AbstractTraceTest;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import requests.FlatFileRequest;
import requests.RouteBuilder;
import requests.SafaRequest;

/**
 * Tests that generated trace links are able to be reviewed.
 */
class TestLinkApproval extends AbstractTraceTest {

    @Test
    void ableToCreateAndRetrieveSingleGeneratedLink() throws Exception {
        String sourceName = "RE-8";
        String targetName = "DD-10";
        String artifactSummary = "This is a summary.";
        String artifactBody = "This is a body.";
        double score = 0.2;

        // Step - Create project, version, source/target artifacts, and generated link between them.
        Project project = dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, "A")
            .newType(projectName, "B")
            .newArtifactAndBody(projectName, "A", sourceName, artifactSummary, artifactBody)
            .newArtifactAndBody(projectName, "B", targetName, artifactSummary, artifactBody)
            .newGeneratedTraceLink(projectName, sourceName, targetName, score, 0)
            .getProject(projectName);

        // Step - Get generated links for project version
        String url = getGeneratedLinkEndpoint(dbEntityBuilder.getProjectVersion(projectName, 0));
        JSONArray links = SafaRequest
            .withRoute(url)
            .getWithJsonArray();

        // VP - Verify that single generated link is returned.
        assertThat(links.length()).isEqualTo(1);

        // VP - Verify that link is the same as the one created.
        assertThat(links.getJSONObject(0).getString("sourceName")).isEqualTo(sourceName);
        assertThat(links.getJSONObject(0).getString("targetName")).isEqualTo(targetName);
    }

    @Test
    void testApproveDeclineLinks() throws Exception {
        String sourceName = "RE-8";
        String targetName = "DD-10";
        double score = 0.2;

        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, "A")
            .newType(projectName, "B")
            .newArtifact(projectName, "A", sourceName)
            .newArtifact(projectName, "B", targetName)
            .newGeneratedTraceLink(projectName, sourceName, targetName, score, 0);

        ProjectVersion projectVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        TraceLinkVersion generatedLink = dbEntityBuilder.getTraceLinks(projectName).get(0);

        // VP - Verify that trace link is unreviewed
        Optional<TraceLinkVersion> unreviewedLinkQuery = traceLinkVersionRepository
            .findByProjectVersionAndTraceLink(projectVersion, generatedLink.getTraceLink());
        assertThat(unreviewedLinkQuery).isPresent();
        assertThat(unreviewedLinkQuery.get().getApprovalStatus()).isEqualTo(ApprovalStatus.UNREVIEWED);

        // Step - Set trace link status to approved
        generatedLink.setApprovalStatus(ApprovalStatus.APPROVED);

        // Step - Approve generated trace link
        TraceAppEntity generatedLinkAppEntity = this.traceLinkVersionRepository
            .retrieveAppEntityFromVersionEntity(generatedLink);
        commitService.commit(CommitBuilder
            .withVersion(projectVersion)
            .withModifiedTrace(generatedLinkAppEntity));

        // VP - Verify that trace link is approved
        Optional<TraceLinkVersion> approvedLinkQuery =
            traceLinkVersionRepository.findByProjectVersionAndTraceLink(
                projectVersion,
                generatedLink.getTraceLink());
        assertThat(approvedLinkQuery).isPresent();
        assertThat(approvedLinkQuery.get().getApprovalStatus()).isEqualTo(ApprovalStatus.APPROVED);

        // Step - Set trace link status to decline d
        generatedLink.setApprovalStatus(ApprovalStatus.DECLINED);

        // Step - Commit changes
        TraceAppEntity updatedGeneratedLink = this.traceLinkVersionRepository
            .retrieveAppEntityFromVersionEntity(generatedLink);
        commitService.commit(CommitBuilder
            .withVersion(projectVersion)
            .withModifiedTrace(updatedGeneratedLink));

        // VP - Verify that link is saved.
        Optional<TraceLinkVersion> declinedLinkQuery = traceLinkVersionRepository.findByProjectVersionAndTraceLink(
            projectVersion,
            generatedLink.getTraceLink());
        assertThat(declinedLinkQuery).isPresent();
        assertThat(declinedLinkQuery.get().getApprovalStatus()).isEqualTo(ApprovalStatus.DECLINED);
    }

    /**
     * Tests that client is able to generate trace links
     *
     * @throws Exception If http requests fail
     */
    @Test
    void testGenerateTraceLinks() throws Exception {

        // Step - Create project and version
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        Project project = projectVersion.getProject();

        // Step - Upload flat files and generate some trace links
        FlatFileRequest.updateProjectVersionFromFlatFiles(projectVersion,
            ProjectPaths.Resources.Tests.DefaultProject.V1);

        // Step - Get all trace links that were generated.
        String url = getGeneratedLinkEndpoint(projectVersion);
        JSONArray links = SafaRequest.withRoute(url).getWithJsonArray();
        int numberOfLinks = links.length();

        // Step - Construct list of artifact app entities from the generated links
        List<ArtifactAppEntity> sourceArtifacts = new ArrayList<>();
        List<ArtifactAppEntity> targetArtifacts = new ArrayList<>();

        for (int i = 0; i < links.length(); i++) {
            JSONObject link = links.getJSONObject(i);
            String source = link.getString("sourceName");
            String target = link.getString("targetName");

            ArtifactVersion sourceBody = artifactVersionRepository.getBodiesWithName(project, source).get(0);
            ArtifactVersion targetBody = artifactVersionRepository.getBodiesWithName(project, target).get(0);

            sourceArtifacts.add(artifactVersionRepository.retrieveAppEntityFromVersionEntity(sourceBody));
            targetArtifacts.add(artifactVersionRepository.retrieveAppEntityFromVersionEntity(targetBody));
        }

        // Send to generate route
        String generateRoute = RouteBuilder.withRoute(AppRoutes.Links.GENERATE_LINKS).buildEndpoint();

        JSONObject generateTraceLinkBody = new JSONObject();
        generateTraceLinkBody.put("sourceArtifacts", sourceArtifacts);
        generateTraceLinkBody.put("targetArtifacts", targetArtifacts);

        JSONArray generatedLinks = SafaRequest
            .withRoute(generateRoute)
            .postWithJsonArray(generateTraceLinkBody);

        // VP - Verify that same number of links were generated.
        assertThat(generatedLinks.length()).isPositive();
    }

    /**
     * The following test verifies that a trace link can be created by:
     * 1. Verify that some link does not exist.
     * 2. Committing new trace link
     * 3. Fetching link to verify it exists.
     */
    @Test
    void testCreateTraceLink() throws Exception {
        String sourceName = "D9";
        String targetName = "F21";

        // Step - Create project with artifacts.
        ProjectVersion projectVersion = dbEntityBuilder.newProject(projectName).newVersionWithReturn(projectName);
        FlatFileRequest.updateProjectVersionFromFlatFiles(projectVersion,
            ProjectPaths.Resources.Tests.DefaultProject.V1);

        // VP - Verify that trace does not exist
        Project project = projectVersion.getProject();
        assertTraceDoesNotExist(project, sourceName, targetName);

        // Step - POST trace links creation
        JSONObject traceJson = jsonBuilder.createTrace(sourceName, targetName);
        commitService.commit(
            CommitBuilder
                .withVersion(projectVersion)
                .withAddedTrace(traceJson)
        );

        // VP - Verify that link created
        assertTraceExists(project, sourceName, targetName);
    }
}
