package edu.nd.crc.safa.test.features.traces.logic;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.builders.CommitBuilder;
import edu.nd.crc.safa.test.features.traces.base.AbstractTraceTest;
import edu.nd.crc.safa.test.requests.FlatFileRequest;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.MappingTestService;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that generated trace links are able to be reviewed in subsequent versions after generation
 */
class TestApproveLinkInFutureVersion extends AbstractTraceTest {

    @Test
    void ableToEditGeneratedLinksInFutureVersions() throws Exception {
        String sourceName = "RE-8";
        String targetName = "DD-10";

        // Step - Create base version
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        // Step - Upload before files containing generated links
        FlatFileRequest.updateProjectVersionFromFlatFiles(projectVersion,
            ProjectPaths.Resources.Tests.DefaultProject.V1);

        // Step - Get generated links
        String url = getGeneratedLinkEndpoint(dbEntityBuilder.getProjectVersion(projectName, 0));
        JSONArray links = SafaRequest.withRoute(url).getWithJsonArray();
        JSONObject link = links.getJSONObject(0);

        // Step - Set link to approved
        link.put("approvalStatus", ApprovalStatus.APPROVED);
        TraceAppEntity traceAppEntity = MappingTestService.toClass(link.toString(), TraceAppEntity.class);

        // Step - Commit link change to new version
        ProjectVersion projectVersionLater = dbEntityBuilder.newVersionWithReturn(projectName);
        CommitBuilder commitBuilder = CommitBuilder
            .withVersion(projectVersionLater)
            .withModifiedTrace(traceAppEntity);

        // Step - Commit
        commitService.commit(commitBuilder);

        // VP - Verify that two versions exist of the trace link
        UUID traceLinkId = UUID.fromString(link.getString("traceLinkId"));
        List<TraceLinkVersion> linkVersions = this.traceLinkVersionRepository.findByTraceLinkTraceLinkId(traceLinkId);
        assertThat(linkVersions).hasSize(2);

        // VP - Verify that
        TraceLinkVersion modifiedTraceLinkVersion = linkVersions.get(1);
        assertThat(modifiedTraceLinkVersion.getApprovalStatus()).isEqualTo(ApprovalStatus.APPROVED);
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
        TraceAppEntity updatedGeneratedLinkAppEntity = this.traceLinkVersionRepository
            .retrieveAppEntityFromVersionEntity(generatedLink);
        commitService.commit(CommitBuilder
            .withVersion(projectVersion)
            .withModifiedTrace(updatedGeneratedLinkAppEntity));

        // VP - Verify that link is saved.
        Optional<TraceLinkVersion> declinedLinkQuery = traceLinkVersionRepository.findByProjectVersionAndTraceLink(
            projectVersion,
            generatedLink.getTraceLink());
        assertThat(declinedLinkQuery).isPresent();
        assertThat(declinedLinkQuery.get().getApprovalStatus()).isEqualTo(ApprovalStatus.DECLINED);
    }
}
