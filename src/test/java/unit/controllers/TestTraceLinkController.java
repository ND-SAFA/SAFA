package unit.controllers;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.db.entities.sql.TraceApproval;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.EntityBaseTest;

public class TestTraceLinkController extends EntityBaseTest {

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

        String projectId = entityBuilder.getProject(projectName).getProjectId().toString();
        String url = String.format("/projects/%s/links/generated", projectId);
        JSONObject response = sendGet(url, MockMvcResultMatchers.status().isOk());
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
        sendPut(acceptUrl, new JSONObject(), MockMvcResultMatchers.status().is2xxSuccessful());

        // VP - Verify that trace link is approved
        Optional<TraceLink> approvedLinkQuery = traceLinkRepository.findById(traceLinkId);
        assertThat(approvedLinkQuery.isPresent()).isTrue();
        assertThat(approvedLinkQuery.get().getApprovalStatus()).isEqualTo(TraceApproval.APPROVED);

        // Step - Decline generated link
        String declineUrl = String.format("/projects/links/%s/decline", traceLinkId);
        sendPut(declineUrl, new JSONObject(), MockMvcResultMatchers.status().is2xxSuccessful());
        Optional<TraceLink> declinedLinkQuery = traceLinkRepository.findById(traceLinkId);
        assertThat(declinedLinkQuery.isPresent()).isTrue();
        assertThat(declinedLinkQuery.get().getApprovalStatus()).isEqualTo(TraceApproval.DECLINED);
    }
}
