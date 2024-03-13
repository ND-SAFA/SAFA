package edu.nd.crc.safa.test.features.generation;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.generation.summary.ProjectSummaryService;
import edu.nd.crc.safa.features.generation.summary.SummarizeArtifactRequestDTO;
import edu.nd.crc.safa.features.generation.summary.SummaryService;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.mock.mockito.MockBean;

public class TestMaxGenerationArtifacts extends ApplicationBaseTest {

    @MockBean
    private SummaryService summaryService;

    @MockBean
    private ProjectSummaryService projectSummaryService;

    @Value("${limits.summarization_max_project_size}")
    private int maxProjectSize;

    private ProjectVersion projectVersion;
    private ArtifactType type;
    private List<UUID> artifactIds;

    @BeforeEach
    public void setupTest() {
        Project project = dbEntityBuilder.newProjectWithReturn("Test project name");
        projectVersion = dbEntityBuilder.newVersionWithReturn(project.getName());
        type = dbEntityBuilder.newTypeAndReturn(project.getName(), "type");
        artifactIds = new ArrayList<>();

        for (int i = 0; i < maxProjectSize + 1; ++i) {
            String artifactName = "artifact" + i;
            ArtifactVersion artifact = dbEntityBuilder.newArtifact(project.getName(), type.getName(), artifactName)
                .newArtifactBodyWithReturn(project.getName(), 0, ModificationType.ADDED, artifactName, "", "");
            artifactIds.add(artifact.getArtifact().getArtifactId());
        }
    }

    @Test
    public void testGenerationProceedsWithLessThanMaxArtifacts() {
        artifactIds.remove(artifactIds.size() - 1);
        List<String> result = doSuccessfulGeneration();
        assertThat(result).isNotNull();
    }

    @Test
    public void testGenerationFailsWithMoreThanMaxArtifacts() {
        JSONObject result = doFailedGeneration();

        JSONArray additionErrors = result.getJSONArray("additionalErrors");
        assertThat(additionErrors.length()).isEqualTo(1);
        assertThat(additionErrors.getString(0)).contains("at most " + maxProjectSize + " artifacts");
    }

    private List<String> doSuccessfulGeneration() {
        SummarizeArtifactRequestDTO body = new SummarizeArtifactRequestDTO();
        body.setArtifacts(artifactIds);

        return SafaRequest.withRoute(AppRoutes.Summarize.SUMMARIZE_ARTIFACTS)
            .withVersion(projectVersion)
            .postAndParseResponse(body, new TypeReference<>() {
            });
    }

    private JSONObject doFailedGeneration() {
        SummarizeArtifactRequestDTO body = new SummarizeArtifactRequestDTO();
        body.setArtifacts(artifactIds);

        return SafaRequest.withRoute(AppRoutes.Summarize.SUMMARIZE_ARTIFACTS)
            .withVersion(projectVersion)
            .postWithJsonObject(body, status().is(403));
    }
}
