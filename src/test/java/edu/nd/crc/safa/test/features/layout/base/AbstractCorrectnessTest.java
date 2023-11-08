package edu.nd.crc.safa.test.features.layout.base;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.services.MappingTestService;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.json.JSONObject;

public abstract class AbstractCorrectnessTest extends ApplicationBaseTest {
    protected String projectName = "project name";
    protected String artifactType = "Requirement";
    protected String artifactBody = "This is body";

    protected String a1Name = "R1";
    protected String a2Name = "R2";
    protected String a3Name = "R3";

    protected ProjectVersion projectVersion;

    public ProjectCommitDefinition createProject() throws Exception {
        this.jsonBuilder.withProject(projectName, projectName, "");
        this.projectVersion = this.dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        this.jsonBuilder.withProject(projectName, projectName, "");
        return commitService.commit(CommitBuilder.withVersion(projectVersion)
            .withAddedArtifact(createArtifact(a1Name))
            .withAddedArtifact(createArtifact(a2Name))
            .withAddedArtifact(createArtifact(a3Name))
            .withAddedTrace(jsonBuilder.createTrace(a2Name, a1Name))
            .withAddedTrace(jsonBuilder.createTrace(a3Name, a1Name)));
    }

    /**
     * Makes the following assertions about the following structure:
     * - Root node is above both children
     * - Children have the same height
     *
     * @param rootPos        The position of the root node.
     * @param firstChildPos  The position of one of the children.
     * @param secondChildPos The position of the other child.
     */
    protected void assertLayoutCorrectness(LayoutPosition rootPos,
                                           LayoutPosition firstChildPos,
                                           LayoutPosition secondChildPos) {
        assertThat(rootPos.getY()).isLessThan(firstChildPos.getY());
        assertThat(rootPos.getY()).isLessThan(secondChildPos.getY());
        assertThat(firstChildPos.getY()).isEqualTo(secondChildPos.getY());
    }

    protected JSONObject createArtifact(String artifactName) {
        return jsonBuilder.withArtifactAndReturn(
            projectName, null, artifactName, artifactType, artifactBody
        );
    }

    protected LayoutPosition getPosition(ProjectAppEntity project, String artifactName) {
        ArtifactAppEntity artifact =
            project
                .getArtifacts()
                .stream()
                .filter(a -> a.getName().equals(artifactName))
                .collect(Collectors.toList())
                .get(0);
        UUID id = artifact.getId();
        return project.getLayout().get(id);
    }

    protected LayoutPosition getLayoutPositionInDocument(ProjectAppEntity project,
                                                         UUID documentId,
                                                         String artifactName) {
        UUID artifactId = retrievalService.getArtifactId(project.getArtifacts(), artifactName);
        List<DocumentAppEntity> documents = project.getDocuments()
            .stream()
            .filter(d -> d.getDocumentId().equals(documentId))
            .collect(Collectors.toList());

        if (documents.size() == 0) {
            throw new SafaError("Document id not found in project:" + documentId);
        } else if (documents.size() > 1) {
            throw new IllegalStateException("Found more than one document with id:" + documentId);
        }

        Map<UUID, LayoutPosition> documentLayout = documents.get(0).getLayout();

        if (!documentLayout.containsKey(artifactId)) {
            throw new IllegalArgumentException("Could not find layout position for artifact id:" + artifactId);
        }
        return documentLayout.get(artifactId);
    }

    protected List<UUID> getArtifactIds(ProjectCommitDefinition projectCommitDefinition) {
        return new ArrayList<>(getArtifactNameToIdMap(projectCommitDefinition).values());
    }

    protected UUID getArtifactIdFromProjectCommit(ProjectCommitDefinition projectCommitDefinition, String artifactName) {
        return getArtifactNameToIdMap(projectCommitDefinition).get(artifactName);
    }

    protected List<LayoutPosition> getArtifactPositionsInDocument(
        ProjectCommitDefinition projectCommitDefinition,
        JSONObject documentJson,
        List<String> artifactNames) throws JsonProcessingException {
        DocumentAppEntity document = MappingTestService.toClass(documentJson.toString(), DocumentAppEntity.class);
        return artifactNames
            .stream()
            .map(artifactName -> {
                UUID artifactId = getArtifactIdFromProjectCommit(projectCommitDefinition, artifactName);
                return document.getLayout().get(artifactId);
            })
            .collect(Collectors.toList());
    }

    private Map<String, UUID> getArtifactNameToIdMap(ProjectCommitDefinition projectCommitDefinition) {
        Map<String, UUID> name2id = new Hashtable<>();
        projectCommitDefinition.getArtifacts().getAdded().forEach(artifact -> {
            name2id.put(artifact.getName(), artifact.getId());
        });
        return name2id;
    }
}
