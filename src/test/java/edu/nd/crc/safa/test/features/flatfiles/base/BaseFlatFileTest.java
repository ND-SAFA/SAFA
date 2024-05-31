package edu.nd.crc.safa.test.features.flatfiles.base;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.HashMap;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Supplier;

import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntityType;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.common.DefaultProjectConstants;

import org.json.JSONArray;
import org.json.JSONObject;

public abstract class BaseFlatFileTest extends ApplicationBaseTest {

    public Project verifyDefaultProjectCreationResponse(JSONObject creationResponse) {

        // VP - Project id is not null
        assertThat(creationResponse).as("uploadedFiles non-null").isNotNull();
        String projectId = creationResponse.getString("projectId");

        // VP - Project with id was created
        Project project = projectRepository.findByProjectId(UUID.fromString(projectId));
        assertThat(project).as("project was created").isNotNull();

        // VP - Artifacts present in response
        assertThat(creationResponse.getJSONArray("artifacts").length())
            .as("all artifacts confirmed")
            .isEqualTo(DefaultProjectConstants.Entities.N_ARTIFACTS);

        // VP - Traces present in response
        JSONArray traces = creationResponse.getJSONArray("traces");
        assertThat(traces.length())
            .as("all traces parsed")
            .isGreaterThanOrEqualTo(DefaultProjectConstants.Entities.N_LINKS);

        int nManual = (int) traces
            .toList()
            .stream()
            .filter((traceJson) ->
                ((HashMap) traceJson).get("traceType").equals(TraceType.MANUAL.toString())
            ).count();
        assertThat(nManual)
            .as("manual traced confirmed")
            .isEqualTo(DefaultProjectConstants.Entities.N_LINKS);

        // VP - Errors are present in response
        JSONObject errors = creationResponse.getJSONObject("errors");
        assertThat(errors.getJSONArray("tim").length())
            .as("tim file error")
            .isZero();
        assertThat(errors.getJSONArray("artifacts").length())
            .as("artifact parsing errors")
            .isZero();
        assertThat(errors.getJSONArray("traces").length())
            .as("trace link errors")
            .isEqualTo(1);

        // VP - Verify invalid trace link detected
        JSONObject traceError = errors.getJSONArray("traces").getJSONObject(0);
        assertThat(traceError.get("errorId")).isNotNull();
        assertThat(traceError.getString("message")).contains("FX1");
        assertThat(traceError.get("activity")).isNotNull();

        // VP - Project warnings present in response
        JSONObject projectWarnings = creationResponse.getJSONObject("warnings");
        assertThat(projectWarnings.keySet()).isEmpty();

        return project;
    }

    public void verifyDefaultProjectEntities(Project project) {
        // VP 3 - Resources were created
        ProjectVersion projectVersion = verifyNumberOfItems("Project Version",
            () -> projectVersionRepository.findByProject(project), 1).get(0);
        assertThat(projectVersion).as("project version created").isNotNull();

        // VP - Project types
        verifyNumberOfItems("Artifact Types",
            () -> artifactTypeRepository.findByProject(project), DefaultProjectConstants.Entities.N_TYPES);

        // VP - requirements created
        verifyArtifactType(project, "requirement", DefaultProjectConstants.Entities.N_REQUIREMENTS);
        verifyArtifactType(project, "design", DefaultProjectConstants.Entities.N_DESIGNS);
        verifyArtifactType(project, "hazard", DefaultProjectConstants.Entities.N_HAZARDS);
        verifyArtifactType(project, "environmentalassumption", DefaultProjectConstants.Entities.N_ENV_ASSUMPTIONS);

        // VP - Verify that total number of artifacts is as expected.
        verifyNumberOfItems("Artifacts",
            () -> artifactRepository.getProjectArtifacts(project.getId()),
            DefaultProjectConstants.Entities.N_ARTIFACTS);

        // VP - Verify that artifact body created for each artifact
        verifyNumberOfItems("Artifact Version Entity",
            () -> artifactVersionRepository.findByProjectVersion(projectVersion),
            DefaultProjectConstants.Entities.N_ARTIFACTS);

        // VP - Verify that link referencing unknown artifact FX1 in R2R
        CommitError error = verifyNumberOfItems("Trace Errors",
            () -> commitErrorRepository.findByProjectVersion(projectVersion),
            1).get(0);
        assertThat(error.getApplicationActivity()).isEqualTo(ProjectEntityType.TRACES);
        assertThat(error.getDescription()).contains("FX1");

        // VP - Verify that remaining links were created.
        verifyNumberOfItems("Trace Links",
            () -> traceLinkVersionRepository.getApprovedLinksInVersion(projectVersion),
            DefaultProjectConstants.Entities.N_LINKS);
    }

    private void verifyArtifactType(Project project, String typeName, int nArtifacts) {
        // VP - Verify that type is created
        String typeTestName = "Artifact type created: " + typeName;
        Optional<ArtifactType> artifactType = artifactTypeRepository.findByProjectAndNameIgnoreCase(project, typeName);
        assertThat(artifactType).as(typeTestName).isPresent();

        // VP - Verify that # of artifact is as expected.
        verifyNumberOfItems(typeName,
            () -> artifactRepository.findByProjectIdAndType(project.getId(), artifactType.orElseThrow()),
            nArtifacts);
    }

    protected <T> List<T> verifyNumberOfItems(String itemName,
                                              Supplier<List<T>> findFunction,
                                              int nItems) {
        String testName = "Verified # of" + itemName + ":" + nItems;
        List<T> items = findFunction.get();
        assertThat(items)
            .as(testName)
            .hasSize(nItems);
        return items;
    }
}
