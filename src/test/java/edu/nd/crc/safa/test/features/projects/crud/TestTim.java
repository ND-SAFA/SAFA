package edu.nd.crc.safa.test.features.projects.crud;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.services.ProjectRetrievalService;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;
import edu.nd.crc.safa.features.types.entities.TypeAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestTim extends ApplicationBaseTest {

    private final String type1Name = "type1";
    private final String type2Name = "type2";
    private final String artifact1Name = "type1Artifact";
    private final String artifact2Name = "type2Artifact1";
    private final String artifact3Name = "type2Artifact2";
    private final Map<String, Integer> typeCounts = Map.of(type1Name, 1, type2Name, 2);
    @Autowired
    private ProjectRetrievalService projectRetrievalService;

    @Test
    public void testTypesNoArtifacts() {
        ProjectVersion version = initialSetup();

        ProjectAppEntity project = projectRetrievalService.getProjectAppEntity(getCurrentUser(), version);
        List<TypeAppEntity> types = project.getArtifactTypes();

        assertNoTypes(types);
    }

    @Test
    public void testTypesWithArtifacts() {
        ProjectVersion version = initialSetup();
        createArtifacts(version);

        ProjectAppEntity project = projectRetrievalService.getProjectAppEntity(getCurrentUser(), version);
        List<TypeAppEntity> types = project.getArtifactTypes();

        assertTypes(types);
    }

    @Test
    public void testTracesNoArtifacts() {
        ProjectVersion version = initialSetup();

        ProjectAppEntity project = projectRetrievalService.getProjectAppEntity(getCurrentUser(), version);
        List<TraceMatrixAppEntity> traces = project.getTraceMatrices();

        assertEquals(0, traces.size());
    }

    @Test
    public void testTracesWithArtifacts() {
        ProjectVersion version = initialSetup();
        createArtifacts(version);

        ProjectAppEntity project = projectRetrievalService.getProjectAppEntity(getCurrentUser(), version);
        List<TraceMatrixAppEntity> traces = project.getTraceMatrices();

        assertEquals(0, traces.size());
    }

    @Test
    public void testTracesWithArtifactsAndLinks() {
        ProjectVersion version = initialSetup();
        createArtifacts(version);
        createLinks(version);

        ProjectAppEntity project = projectRetrievalService.getProjectAppEntity(getCurrentUser(), version);
        List<TraceMatrixAppEntity> traces = project.getTraceMatrices();

        assertTraces(traces);
    }

    @Test
    public void testCreatingNewVersion() {
        ProjectVersion version = initialSetup();
        createArtifacts(version);
        createLinks(version);
        version = createProjectVersion();

        ProjectAppEntity project = projectRetrievalService.getProjectAppEntity(getCurrentUser(), version);
        List<TraceMatrixAppEntity> traces = project.getTraceMatrices();
        List<TypeAppEntity> types = project.getArtifactTypes();

        assertTypes(types);
        assertTraces(traces);
    }

    @Test
    public void testDeletedItems() {
        ProjectVersion version = initialSetup();
        createArtifacts(version);
        createLinks(version);

        ProjectAppEntity project = projectRetrievalService.getProjectAppEntity(getCurrentUser(), version);

        version = createProjectVersion();
        deleteLinks(version, project.getTraces());
        deleteArtifacts(version, project.getArtifacts());

        project = projectRetrievalService.getProjectAppEntity(getCurrentUser(), version);
        List<TraceMatrixAppEntity> traces = project.getTraceMatrices();
        List<TypeAppEntity> types = project.getArtifactTypes();

        assertNoTypes(types);
        assertNoTraces(traces);
    }

    @Test
    public void testApprovedLinks() {
        ProjectVersion version = initialSetup();
        createArtifacts(version);
        createLinks(version);

        ProjectAppEntity project = projectRetrievalService.getProjectAppEntity(getCurrentUser(), version);

        version = createProjectVersion();
        approveLinks(version, project.getTraces());

        project = projectRetrievalService.getProjectAppEntity(getCurrentUser(), version);
        List<TraceMatrixAppEntity> traces = project.getTraceMatrices();

        assertApprovedTraces(traces);
    }

    private void assertTypes(List<TypeAppEntity> types) {
        List<String> notFound = new ArrayList<>(List.of(type1Name, type2Name));
        for (TypeAppEntity type : types) {
            assertTrue(notFound.remove(type.getName()));
            assertEquals(typeCounts.get(type.getName()), type.getCount());
        }

        assertEquals(0, notFound.size());
    }

    private void assertNoTypes(List<TypeAppEntity> types) {
        List<String> notFound = new ArrayList<>(List.of(type1Name, type2Name));
        for (TypeAppEntity type : types) {
            assertTrue(notFound.remove(type.getName()));
            assertEquals(0, type.getCount());
        }

        assertEquals(0, notFound.size());
    }

    private void assertTraces(List<TraceMatrixAppEntity> traces) {
        assertEquals(2, traces.size());
        for (TraceMatrixAppEntity trace : traces) {
            if (type1Name.equalsIgnoreCase(trace.getSourceType())
                && type2Name.equalsIgnoreCase(trace.getTargetType())) {
                assertEquals(2, trace.getCount());
                assertEquals(1, trace.getGeneratedCount());
                assertEquals(0, trace.getApprovedCount());
            } else if (type2Name.equalsIgnoreCase(trace.getSourceType())
                && type2Name.equalsIgnoreCase(trace.getTargetType())) {
                assertEquals(1, trace.getCount());
                assertEquals(1, trace.getGeneratedCount());
                assertEquals(1, trace.getApprovedCount());
            } else {
                fail(String.format("Unknown trace pair %s -> %s", trace.getSourceType(), trace.getTargetType()));
            }
        }
    }

    private void assertApprovedTraces(List<TraceMatrixAppEntity> traces) {
        assertEquals(2, traces.size());
        for (TraceMatrixAppEntity trace : traces) {
            if (type1Name.equalsIgnoreCase(trace.getSourceType())
                && type2Name.equalsIgnoreCase(trace.getTargetType())) {
                assertEquals(2, trace.getCount());
                assertEquals(1, trace.getGeneratedCount());
                assertEquals(1, trace.getApprovedCount());
            } else if (type2Name.equalsIgnoreCase(trace.getSourceType())
                && type2Name.equalsIgnoreCase(trace.getTargetType())) {
                assertEquals(1, trace.getCount());
                assertEquals(1, trace.getGeneratedCount());
                assertEquals(1, trace.getApprovedCount());
            } else {
                fail(String.format("Unknown trace pair %s -> %s", trace.getSourceType(), trace.getTargetType()));
            }
        }
    }

    private void assertNoTraces(List<TraceMatrixAppEntity> traces) {
        assertEquals(2, traces.size());
        for (TraceMatrixAppEntity trace : traces) {
            if (type1Name.equalsIgnoreCase(trace.getSourceType())
                && type2Name.equalsIgnoreCase(trace.getTargetType())) {
                assertEquals(0, trace.getCount());
                assertEquals(0, trace.getGeneratedCount());
                assertEquals(0, trace.getApprovedCount());
            } else if (type2Name.equalsIgnoreCase(trace.getSourceType())
                && type2Name.equalsIgnoreCase(trace.getTargetType())) {
                assertEquals(0, trace.getCount());
                assertEquals(0, trace.getGeneratedCount());
                assertEquals(0, trace.getApprovedCount());
            } else {
                fail(String.format("Unknown trace pair %s -> %s", trace.getSourceType(), trace.getTargetType()));
            }
        }
    }

    private ArtifactAppEntity createArtifact(String typeName, String name) {
        return new ArtifactAppEntity(null, typeName, name, "", "", new HashMap<>());
    }

    private ProjectVersion createProjectVersion() {
        return dbEntityBuilder.newVersionWithReturn(projectName);
    }

    private ProjectVersion initialSetup() {
        dbEntityBuilder.newProject(projectName)
            .newType(projectName, type1Name)
            .newType(projectName, type2Name);
        return createProjectVersion();
    }

    private void createArtifacts(ProjectVersion version) {
        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition(null, version, true);
        projectCommitDefinition.addArtifact(ModificationType.ADDED, createArtifact(type1Name, artifact1Name));
        projectCommitDefinition.addArtifact(ModificationType.ADDED, createArtifact(type2Name, artifact2Name));
        projectCommitDefinition.addArtifact(ModificationType.ADDED, createArtifact(type2Name, artifact3Name));
        serviceProvider.getCommitService().performCommit(projectCommitDefinition, getCurrentUser());
    }

    private void deleteArtifacts(ProjectVersion version, List<ArtifactAppEntity> artifacts) {
        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition(null, version, true);
        projectCommitDefinition.addArtifacts(ModificationType.REMOVED, artifacts);
        serviceProvider.getCommitService().performCommit(projectCommitDefinition, getCurrentUser());
    }

    private TraceAppEntity createTrace(String sourceName, String targetName, ApprovalStatus status, TraceType type) {
        return new TraceAppEntity(null, sourceName, null, targetName, null, status, 1, type, true, "");
    }

    private void createLinks(ProjectVersion version) {
        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition(null, version, true);
        projectCommitDefinition.addTrace(ModificationType.ADDED,
            createTrace(artifact1Name, artifact2Name, ApprovalStatus.APPROVED, TraceType.MANUAL));
        projectCommitDefinition.addTrace(ModificationType.ADDED,
            createTrace(artifact1Name, artifact3Name, ApprovalStatus.UNREVIEWED, TraceType.GENERATED));
        projectCommitDefinition.addTrace(ModificationType.ADDED,
            createTrace(artifact2Name, artifact3Name, ApprovalStatus.APPROVED, TraceType.GENERATED));
        serviceProvider.getCommitService().performCommit(projectCommitDefinition, getCurrentUser());
    }

    private void deleteLinks(ProjectVersion version, List<TraceAppEntity> links) {
        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition(null, version, true);
        projectCommitDefinition.addTraces(ModificationType.REMOVED, links);
        serviceProvider.getCommitService().performCommit(projectCommitDefinition, getCurrentUser());
    }

    private void approveLinks(ProjectVersion version, List<TraceAppEntity> links) {
        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition(null, version, true);
        for (TraceAppEntity link : links) {
            link.setApprovalStatus(ApprovalStatus.APPROVED);
            projectCommitDefinition.addTrace(ModificationType.MODIFIED, link);
        }
        serviceProvider.getCommitService().performCommit(projectCommitDefinition, getCurrentUser());
    }
}
