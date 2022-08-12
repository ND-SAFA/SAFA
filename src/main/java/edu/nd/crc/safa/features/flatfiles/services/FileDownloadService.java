package edu.nd.crc.safa.features.flatfiles.services;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.FTAType;
import edu.nd.crc.safa.features.artifacts.entities.SafetyCaseType;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.flatfiles.entities.common.AbstractArtifactFile;
import edu.nd.crc.safa.features.flatfiles.entities.common.AbstractTraceFile;
import edu.nd.crc.safa.features.flatfiles.entities.common.ProjectEntities;
import edu.nd.crc.safa.features.flatfiles.entities.common.TraceMaps;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.AppEntityRetrievalService;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.javatuples.Pair;
import org.json.JSONObject;
import org.springframework.stereotype.Service;

/**
 * Downloads project entities as flat files.
 */
@Service
@AllArgsConstructor
public class FileDownloadService {
    private final AppEntityRetrievalService appEntityRetrievalService;

    public List<File> downloadProjectFiles(ProjectVersion projectVersion, String fileType) throws Exception {
        Project project = projectVersion.getProject();
        ProjectAppEntity projectAppEntity =
            this.appEntityRetrievalService.retrieveProjectAppEntityAtProjectVersion(projectVersion);
        List<File> projectFiles = new ArrayList<>();

        ProjectEntities projectEntityMaps = new ProjectEntities(projectAppEntity);
        List<ArtifactFileIdentifier> artifactFiles = writeArtifactFiles(fileType, project, projectEntityMaps,
            projectFiles);
        List<TraceFileIdentifier> traceFiles = writeTraceFiles(fileType, project, projectFiles,
            projectAppEntity,
            projectEntityMaps);
        File timFile = writeTimFile(project, artifactFiles, traceFiles);
        projectFiles.add(timFile);
        return projectFiles;
    }

    private List<TraceFileIdentifier> writeTraceFiles(String fileType,
                                                      Project project,
                                                      List<File> projectFiles,
                                                      ProjectAppEntity projectAppEntity,
                                                      ProjectEntities projectEntityMaps) throws Exception {
        TraceMaps traceMaps = new TraceMaps(projectAppEntity, projectEntityMaps);
        List<TraceFileIdentifier> traceFiles = new ArrayList<>();
        for (String sourceType : traceMaps.getSourceTypes()) {
            for (String targetType : traceMaps.getTargetTypes(sourceType)) {
                // Step - Create file
                String fileName = String.format("%s2%s.%s", sourceType, targetType, fileType);
                String pathToFile = ProjectPaths.getPathToProjectFile(project, fileName);
                File traceFileOutput = new File(pathToFile);

                // Step - Create trace file
                List<TraceAppEntity> traces = traceMaps.getTracesBetweenTypes(sourceType, targetType);
                AbstractTraceFile<?> traceFile = DataFileBuilder.createTraceFileParser(pathToFile, traces);
                TraceFileIdentifier traceFileIdentifier = new TraceFileIdentifier(fileName, sourceType, targetType);
                traceFiles.add(traceFileIdentifier);
                traceFile.export(traceFileOutput);

                projectFiles.add(traceFileOutput);
            }
        }
        return traceFiles;
    }

    private List<ArtifactFileIdentifier> writeArtifactFiles(String fileType,
                                                            Project project,
                                                            ProjectEntities projectEntityMaps,
                                                            List<File> projectFiles) throws Exception {
        List<ArtifactFileIdentifier> artifactFiles = new ArrayList<>();
        for (String artifactType : projectEntityMaps.getArtifactTypes()) {
            String fileName = String.format("%s.%s", artifactType, fileType);
            String pathToFile = ProjectPaths.getPathToProjectFile(project, fileName);

            File artifactFileOutput = new File(pathToFile);
            List<ArtifactAppEntity> artifacts = projectEntityMaps.getArtifactsInType(artifactType);
            DocumentType documentType = getDocumentTypeFromType(artifactType);
            AbstractArtifactFile<?> artifactFile = DataFileBuilder.createArtifactFileParser(artifactType,
                pathToFile,
                documentType,
                artifacts);
            ArtifactFileIdentifier artifactFileIdentifier = new ArtifactFileIdentifier(fileName,
                artifactType,
                documentType);
            artifactFiles.add(artifactFileIdentifier);
            artifactFile.export(artifactFileOutput);
            projectFiles.add(artifactFileOutput);
        }
        return artifactFiles;
    }

    private <T extends Enum<T>> DocumentType getDocumentTypeFromType(String artifactType) {
        List<Pair<DocumentType, Class<T>>> documentValues = new ArrayList<>();
        documentValues.add(new Pair<>(DocumentType.SAFETY_CASE, (Class<T>) SafetyCaseType.class));
        documentValues.add(new Pair<>(DocumentType.FTA, (Class<T>) FTAType.class));

        for (Pair<DocumentType, Class<T>> documentTypeClassPair : documentValues) {
            Class<T> enumClass = documentTypeClassPair.getValue1();
            boolean hasMatch = Arrays
                .stream(enumClass.getEnumConstants())
                .anyMatch(enumValue -> enumValue.toString()
                    .equals(artifactType));
            if (hasMatch) {
                return documentTypeClassPair.getValue0();
            }
        }
        return DocumentType.ARTIFACT_TREE;
    }

    private File writeTimFile(Project project,
                              List<ArtifactFileIdentifier> artifactFiles,
                              List<TraceFileIdentifier> traceFiles) throws IOException {
        String pathToFile = ProjectPaths.getPathToProjectFile(project, ProjectVariables.TIM_FILENAME);
        File timFile = new File(pathToFile);
        JSONObject fileContent = new JSONObject();
        JSONObject dataFiles = new JSONObject();
        for (ArtifactFileIdentifier artifactFileIdentifier : artifactFiles) {
            JSONObject artifactDefinition = new JSONObject();
            artifactDefinition.put("File", artifactFileIdentifier.getFileName());
            artifactDefinition.put("Type", artifactFileIdentifier.getDocumentType().toString());
            dataFiles.put(artifactFileIdentifier.getArtifactType(), artifactDefinition);
        }

        for (TraceFileIdentifier traceFileIdentifier : traceFiles) {
            JSONObject traceDefinition = new JSONObject();
            String source = traceFileIdentifier.getSource();
            String target = traceFileIdentifier.getTarget();
            String title = String.format("%sTo%s", source, target);
            traceDefinition.put("Source", traceFileIdentifier.getSource());
            traceDefinition.put("Target", traceFileIdentifier.getTarget());
            traceDefinition.put("File", traceFileIdentifier.getFileName());
            fileContent.put(title, traceDefinition);
        }
        fileContent.put("DataFiles", dataFiles);
        FileUtilities.writeToFile(timFile, fileContent.toString());
        return timFile;
    }

    @AllArgsConstructor
    @Data
    static class ArtifactFileIdentifier {
        String fileName;
        String artifactType;
        DocumentType documentType;
    }

    @AllArgsConstructor
    @Data
    static class TraceFileIdentifier {
        String fileName;
        String source;
        String target;
    }
}
