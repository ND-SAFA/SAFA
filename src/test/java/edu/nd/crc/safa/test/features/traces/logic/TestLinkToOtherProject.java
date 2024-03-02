package edu.nd.crc.safa.test.features.traces.logic;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.nio.charset.StandardCharsets;
import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.jobs.controllers.JobController;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaMultiPartRequest;
import edu.nd.crc.safa.test.services.CommitTestService;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

import org.apache.http.entity.ContentType;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mock.web.MockMultipartFile;

public class TestLinkToOtherProject extends ApplicationBaseTest {

    @Autowired
    private JobController jobController;

    @Test
    public void testLinksCannotBeMadeBetweenProjects() throws Exception {
        Project project1 = dbEntityBuilder.newProjectWithReturn("Project 1");
        ArtifactType type = dbEntityBuilder.newTypeAndReturn(project1.getName(), "type");
        ProjectVersion project1Version = dbEntityBuilder.newVersionWithReturn(project1.getName());

        ArtifactAppEntity artifactDefinition1 = new ArtifactAppEntity();
        ArtifactAppEntity artifactDefinition2 = new ArtifactAppEntity();
        artifactDefinition1.setName("1");
        artifactDefinition1.setType(type.getName());
        artifactDefinition2.setName("2");
        artifactDefinition2.setType(type.getName());

        TraceAppEntity trace = new TraceAppEntity(artifactDefinition1.getName(), artifactDefinition2.getName());

        ProjectCommitDefinition commit =
            CommitTestService.commit(
                CommitBuilder.withVersion(project1Version)
                    .withAddedArtifact(artifactDefinition1)
                    .withAddedArtifact(artifactDefinition2)
                    .withAddedTrace(trace));

        List<ArtifactAppEntity> artifacts = commit.getArtifactList(ModificationType.ADDED);
        List<TraceAppEntity> traces = commit.getTraces().getAdded();

        // This has to be done differently since the json upload is how the bug occurred
        String timContents = "{\"artifacts\":[{\"type\":\"User Story\",\"fileName\":\"User Story.json\"},{\"type\":\"code\",\"fileName\":\"code.json\"}],\"traces\":[{\"sourceType\":\"code\",\"targetType\":\"User Story\",\"fileName\":\"code2User Story.json\",\"generateLinks\":false,\"generationMethod\":null}]}";
        String codeContents = "{\"artifacts\":[{\"summary\":\"\",\"isCode\":false,\"name\":\"1\",\"attributes\":{},\"id\":null,\"body\":\"\",\"type\":\"type\",\"documentIds\":[]}]}";
        String userStoryContents = "{\"artifacts\":[{\"summary\":\"\",\"isCode\":false,\"name\":\"2\",\"attributes\":{},\"id\":null,\"body\":\"\",\"type\":\"type\",\"documentIds\":[]}]}";
        String traceContents = "{\"traces\":[{\"sourceId\":\"" + artifacts.get(0).getId() + "\",\"approvalStatus\":\"APPROVED\",\"score\":0.95,\"traceLinkId\":" + traces.get(0).getId() + ",\"targetName\":\"2\",\"visible\":true,\"targetId\":\"" + artifacts.get(1).getId() +"\",\"traceType\":\"GENERATED\",\"sourceName\":\"1\",\"id\":\"" + traces.get(0).getId() + "\",\"explanation\":\"\"}]}";

        List<MockMultipartFile> files =
            List.of(
                new MockMultipartFile("files", "tim.json", ContentType.APPLICATION_JSON.getMimeType(), timContents.getBytes(StandardCharsets.UTF_8)),
                new MockMultipartFile("files", "code.json", ContentType.APPLICATION_JSON.getMimeType(), codeContents.getBytes(StandardCharsets.UTF_8)),
                new MockMultipartFile("files", "User Story.json", ContentType.APPLICATION_JSON.getMimeType(), userStoryContents.getBytes(StandardCharsets.UTF_8)),
                new MockMultipartFile("files", "code2User Story.json", ContentType.APPLICATION_JSON.getMimeType(), traceContents.getBytes(StandardCharsets.UTF_8))
            );

        JSONObject otherArgs = new JSONObject();
        otherArgs.put("name", "Project 2");
        otherArgs.put("description", "desc");

        JSONObject response = SafaMultiPartRequest.withRoute(AppRoutes.Jobs.Projects.PROJECT_BULK_UPLOAD)
                .sendRequestWithFiles(files, status().is2xxSuccessful(), otherArgs);

        //UUID versionId = serviceProvider.getJobService().getJobById(jobId).getCompletedEntityId();
    }

    private void createTrace() {}
}
