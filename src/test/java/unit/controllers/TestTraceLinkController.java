package unit.controllers;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceApproval;
import edu.nd.crc.safa.server.entities.db.TraceLink;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

public class TestTraceLinkController extends ApplicationBaseTest {

    @Test
    public void testGetGeneratedLinks() throws Exception {
        String projectName = "test-project";
        String sourceName = "RE-8";
        String targetName = "DD-10";
        double score = 0.2;

        entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, "A")
            .newType(projectName, "B")
            .newArtifact(projectName, "A", sourceName)
            .newArtifact(projectName, "B", targetName)
            .newGeneratedTraceLink(projectName, sourceName, targetName, score);

        String url = getGeneratedLinkEndpoint(entityBuilder.getProjectVersion(projectName, 0));
        JSONObject response = sendGet(url, status().isOk());
        JSONArray links = response.getJSONArray("body");
        assertThat(links.length()).isEqualTo(1);
        assertThat(links.getJSONObject(0).getString("source")).isEqualTo(sourceName);
        assertThat(links.getJSONObject(0).getString("target")).isEqualTo(targetName);
    }

    @Test
    public void testApproveDeclineLinks() throws Exception {
        String projectName = "test-project";
        String sourceName = "RE-8";
        String targetName = "DD-10";
        double score = 0.2;

        entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, "A")
            .newType(projectName, "B")
            .newArtifact(projectName, "A", sourceName)
            .newArtifact(projectName, "B", targetName)
            .newGeneratedTraceLink(projectName, sourceName, targetName, score);

        TraceLink generatedLink = entityBuilder.getTraceLinks(projectName).get(0);
        UUID traceLinkId = generatedLink.getTraceLinkId();

        // VP - Verify that trace link is unreviewed
        Optional<TraceLink> unreviewedLinkQuery = traceLinkRepository.findById(traceLinkId);
        assertThat(unreviewedLinkQuery.isPresent()).isTrue();
        assertThat(unreviewedLinkQuery.get().getApprovalStatus()).isEqualTo(TraceApproval.UNREVIEWED);

        // Step - Approve generated trace link
        String acceptUrl = String.format("/projects/links/%s/approve", traceLinkId);
        sendPut(acceptUrl, new JSONObject(), status().is2xxSuccessful());

        // VP - Verify that trace link is approved
        Optional<TraceLink> approvedLinkQuery = traceLinkRepository.findById(traceLinkId);
        assertThat(approvedLinkQuery.isPresent()).isTrue();
        assertThat(approvedLinkQuery.get().getApprovalStatus()).isEqualTo(TraceApproval.APPROVED);

        // Step - Decline generated link
        String declineUrl = String.format("/projects/links/%s/decline", traceLinkId);
        sendPut(declineUrl, new JSONObject(), status().is2xxSuccessful());
        Optional<TraceLink> declinedLinkQuery = traceLinkRepository.findById(traceLinkId);
        assertThat(declinedLinkQuery.isPresent()).isTrue();
        assertThat(declinedLinkQuery.get().getApprovalStatus()).isEqualTo(TraceApproval.DECLINED);
    }

    @Test
    public void testGenerateTraceLinks() throws Exception {

        // Step - Create project and version
        String projectName = "test-project";
        ProjectVersion projectVersion = entityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        Project project = projectVersion.getProject();

        // Step - Upload flat files and generate some trace links
        uploadFlatFilesToVersion(projectVersion, ProjectPaths.PATH_TO_BEFORE_FILES);

        // Step - Get all trace links that were generated.
        String url = getGeneratedLinkEndpoint(projectVersion);
        JSONObject getGeneratedLinksResponse = sendGet(url, status().isOk());
        JSONArray links = getGeneratedLinksResponse.getJSONArray("body");
        int numberOfLinks = links.length();

        // Step - Construct list of artifact app entities from the generated links
        List<ArtifactAppEntity> sourceArtifacts = new ArrayList<>();
        List<ArtifactAppEntity> targetArtifacts = new ArrayList<>();

        for (int i = 0; i < links.length(); i++) {
            JSONObject link = links.getJSONObject(i);
            String source = link.getString("source");
            String target = link.getString("target");


            ArtifactBody sourceBody = artifactBodyRepository.getBodiesWithName(project, source).get(0);
            ArtifactBody targetBody = artifactBodyRepository.getBodiesWithName(project, target).get(0);

            sourceArtifacts.add(new ArtifactAppEntity(sourceBody));
            targetArtifacts.add(new ArtifactAppEntity(targetBody));
        }

        // Send to generate route
        String generateRoute = "/projects/links/generate";
        JSONObject body = new JSONObject();
        body.put("sourceArtifacts", sourceArtifacts);
        body.put("targetArtifacts", targetArtifacts);

        JSONObject generateLinksResponse = sendPost(generateRoute, body, status().is2xxSuccessful());
        JSONArray generatedLinks = generateLinksResponse.getJSONArray("body");

        // VP - Verify that same number of links were generated.
        assertThat(generatedLinks.length()).isEqualTo(numberOfLinks);
    }

    /**
     * The following test verifies that a trace link can be created.
     */
    @Test
    public void testCreateTraceLink() throws Exception {
        String projectName = "project-name";
        String sourceName = "D9";
        String targetName = "F21";

        // Step - Create project with artifacts.
        ProjectVersion projectVersion = entityBuilder.newProject(projectName).newVersionWithReturn(projectName);
        uploadFlatFilesToVersion(projectVersion, ProjectPaths.PATH_TO_BEFORE_FILES);

        // VP - Verify that trace does not exist
        Project project = projectVersion.getProject();
        assertTraceDoesNotExist(project, sourceName, targetName);

        // Step - POST trace links creation
        String versionId = projectVersion.getVersionId().toString();
        String url = String.format("/projects/versions/%s/links/create/%s/%s", versionId, sourceName, targetName);
        JSONObject response = sendPost(url, new JSONObject(), status().is2xxSuccessful());

        // VP - Verify that no error
        int status = response.getInt("status");
        assertThat(status).isEqualTo(0);

        // VP - Verify that link created
        assertTraceExists(project, sourceName, targetName);
    }

    private void assertTraceExists(Project project, String sourceName, String targetName) {
        assertTraceStatus(project, sourceName, targetName, true);
    }

    private void assertTraceDoesNotExist(Project project, String sourceName, String targetName) {
        assertTraceStatus(project, sourceName, targetName, false);
    }

    private void assertTraceStatus(Project project, String sourceName, String targetName, boolean exists) {
        Optional<TraceLink> traceLinkQuery =
            this.traceLinkRepository.getByProjectAndSourceAndTarget(project,
                sourceName,
                targetName);
        assertThat(traceLinkQuery.isPresent()).isEqualTo(exists);
    }

    private String getGeneratedLinkEndpoint(ProjectVersion projectVersion) {
        return String.format("/projects/%s/links/generated", projectVersion.getProject().getProjectId().toString());
    }
}
