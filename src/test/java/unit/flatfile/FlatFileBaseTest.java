package unit.flatfile;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.HashMap;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Supplier;

import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceType;

import org.json.JSONArray;
import org.json.JSONObject;
import unit.ApplicationBaseTest;
import unit.SampleProjectConstants;

public class FlatFileBaseTest extends ApplicationBaseTest {

    public Project verifyBeforeResponse(JSONObject projectJson) throws Exception {

        // VP - Project id is not null
        assertThat(projectJson).as("uploadedFiles non-null").isNotNull();
        String projectId = projectJson.getString("projectId");

        // VP - Project with id was created
        Project project = projectRepository.findByProjectId(UUID.fromString(projectId));
        assertThat(project).as("project was created").isNotNull();

        // VP - Artifacts present in response
        assertThat(projectJson.getJSONArray("artifacts").length())
            .as("all artifacts confirmed")
            .isEqualTo(SampleProjectConstants.N_ARTIFACTS);

        // VP - Traces present in response
        JSONArray traces = projectJson.getJSONArray("traces");
        assertThat(traces.length())
            .as("all traces confirmed")
            .isGreaterThanOrEqualTo(SampleProjectConstants.N_LINKS);

        int nManual = (int) traces
            .toList()
            .stream()
            .filter((traceJson) ->
                ((HashMap) traceJson).get("traceType").equals(TraceType.MANUAL.toString())
            ).count();
        assertThat(nManual)
            .as("manual traced confirmed")
            .isEqualTo(SampleProjectConstants.N_LINKS);

        // VP - Errors are present in response
        JSONObject errors = projectJson.getJSONObject("errors");
        assertThat(errors.getJSONArray("tim").length())
            .as("tim file error")
            .isEqualTo(0);
        assertThat(errors.getJSONArray("artifacts").length())
            .as("artifact parsing errors")
            .isEqualTo(0);
        assertThat(errors.getJSONArray("traces").length())
            .as("trace link errors")
            .isEqualTo(1);

        JSONObject traceError = errors.getJSONArray("traces").getJSONObject(0);
        assertThat(traceError.get("errorId")).isNotNull();
        assertThat(traceError.get("message")).isNotNull();
        assertThat(traceError.get("activity")).isNotNull();

        // VP - Project warnings present in response
        JSONObject projectWarnings = projectJson.getJSONObject("warnings");
        assertThat(projectWarnings.keySet().size()).isGreaterThanOrEqualTo(1);

        return project;
    }

    public void verifyDefaultProjectEntities(Project project) {
        // VP 3 - Resources were created
        ProjectVersion projectVersion = verifyNumberOfItems("Project Version",
            () -> projectVersionRepository.findByProject(project), 1).get(0);
        assertThat(projectVersion).as("project version created").isNotNull();

        // VP - Project types
        verifyNumberOfItems("Artifact Types",
            () -> artifactTypeRepository.findByProject(project), SampleProjectConstants.N_TYPES);

        // VP - requirements created
        verifyArtifactType(project, "requirement", SampleProjectConstants.N_REQUIREMENTS);
        verifyArtifactType(project, "design", SampleProjectConstants.N_DESIGNS);
        verifyArtifactType(project, "hazard", SampleProjectConstants.N_HAZARDS);
        verifyArtifactType(project, "environmentalassumption", SampleProjectConstants.N_ENV_ASSUMPTIONS);

        // VP - Verify that total number of artifacts is as expected.
        verifyNumberOfItems("Artifacts",
            () -> artifactRepository.getProjectArtifacts(project),
            SampleProjectConstants.N_ARTIFACTS);

        // VP - Verify that artifact body created for each artifact
        verifyNumberOfItems("Artifact Version Entity",
            () -> artifactVersionRepository.findByProjectVersion(projectVersion),
            SampleProjectConstants.N_ARTIFACTS);

        // VP - Verify that link referencing unknown artifact FX1 in R2R
        CommitError error = verifyNumberOfItems("Trace Errors",
            () -> commitErrorRepository.findByProjectVersion(projectVersion),
            1).get(0);
        assertThat(error.getApplicationActivity()).isEqualTo(ProjectEntity.TRACES);
        assertThat(error.getDescription()).contains("FX1");

        // VP - Verify that remaining links were created.
        verifyNumberOfItems("Trace Links",
            () -> traceLinkVersionRepository.getApprovedLinksInVersion(projectVersion),
            SampleProjectConstants.N_LINKS);
    }

    private void verifyArtifactType(Project project, String typeName, int nArtifacts) {
        // VP - Verify that type is created
        String typeTestName = "Artifact type created: " + typeName;
        Optional<ArtifactType> artifactType = artifactTypeRepository.findByProjectAndNameIgnoreCase(project, typeName);
        assertThat(artifactType.isPresent()).as(typeTestName).isTrue();

        // VP - Verify that # of artifact is as expected.
        verifyNumberOfItems(typeName,
            () -> artifactRepository.findByProjectAndType(project, artifactType.get()),
            nArtifacts);
    }

    private <T extends Object> List<T> verifyNumberOfItems(String itemName,
                                                           Supplier<List<T>> findFunction,
                                                           int nItems) {
        String testName = "Verified # of" + itemName + ":" + nItems;
        List<T> items = findFunction.get();
        assertThat(items.size())
            .as(testName)
            .isEqualTo(nItems);
        return items;
    }
}
