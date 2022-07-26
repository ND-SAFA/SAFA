package edu.nd.crc.safa.flatfiles.services;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.flatfiles.entities.AbstractArtifactFile;
import edu.nd.crc.safa.flatfiles.entities.AbstractTraceFile;
import edu.nd.crc.safa.flatfiles.entities.ArtifactMaps;
import edu.nd.crc.safa.flatfiles.entities.TraceMaps;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.FTANodeType;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.project.SafetyCaseType;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

import lombok.AllArgsConstructor;
import org.javatuples.Pair;
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

        ArtifactMaps artifactMaps = new ArtifactMaps(projectAppEntity);
        writeArtifactFiles(fileType, project, artifactMaps, projectFiles);
        writeTraceFiles(fileType, project, projectFiles, projectAppEntity, artifactMaps);

        // TODO: Write tim.json
        return projectFiles;
    }

    private void writeTraceFiles(String fileType,
                                 Project project,
                                 List<File> projectFiles,
                                 ProjectAppEntity projectAppEntity,
                                 ArtifactMaps artifactMaps) throws Exception {
        TraceMaps traceMaps = new TraceMaps(projectAppEntity, artifactMaps);
        for (String sourceType : traceMaps.getSourceTypes()) {
            for (String targetType : traceMaps.getTargetTypes(sourceType)) {
                // Step - Create file
                String fileName = String.format("%s2%s.%s", sourceType, targetType, fileType);
                String pathToFile = ProjectPaths.getPathToProjectFile(project, fileName);
                File traceFileOutput = new File(pathToFile);

                // Step - Create trace file
                List<TraceAppEntity> traces = traceMaps.getTracesBetweenTypes(sourceType, targetType);
                AbstractTraceFile<?> traceFileParser = DataFileBuilder.createTraceFileParser(pathToFile, traces);
                System.out.println("Exporting trace file:" + traceFileOutput);
                traceFileParser.export(traceFileOutput);

                projectFiles.add(traceFileOutput);
            }
        }
    }

    private void writeArtifactFiles(String fileType,
                                    Project project,
                                    ArtifactMaps artifactMaps,
                                    List<File> projectFiles) throws Exception {
        for (String artifactType : artifactMaps.getArtifactTypes()) {
            String fileName = String.format("%s.%s", artifactType, fileType);
            String pathToFile = ProjectPaths.getPathToProjectFile(project, fileName);

            File artifactFileOutput = new File(pathToFile);
            List<ArtifactAppEntity> artifacts = artifactMaps.getArtifactsInType(artifactType);
            DocumentType documentType = getDocumentTypeFromType(artifactType);
            AbstractArtifactFile<?> artifactFile = DataFileBuilder.createArtifactFileParser(artifactType,
                pathToFile,
                documentType,
                artifacts);
            artifactFile.export(artifactFileOutput);
            projectFiles.add(artifactFileOutput);
        }
    }

    private <T extends Enum<T>> DocumentType getDocumentTypeFromType(String artifactType) {
        List<Pair<DocumentType, Class<T>>> documentValues = new ArrayList<>();
        documentValues.add(new Pair<>(DocumentType.SAFETY_CASE, (Class<T>) SafetyCaseType.class));
        documentValues.add(new Pair<>(DocumentType.FTA, (Class<T>) FTANodeType.class));
        
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
}
