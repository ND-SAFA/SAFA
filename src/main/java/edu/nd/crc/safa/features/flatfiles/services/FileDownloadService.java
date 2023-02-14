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
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.common.Type2TraceMap;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractArtifactFile;
import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractTraceFile;
import edu.nd.crc.safa.features.flatfiles.parser.tim.TimArtifactDefinition;
import edu.nd.crc.safa.features.flatfiles.parser.tim.TimSchema;
import edu.nd.crc.safa.features.flatfiles.parser.tim.TimTraceDefinition;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectRetrievalService;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import org.javatuples.Pair;
import org.springframework.stereotype.Service;

/**
 * Downloads project entities as flat files.
 */
@Service
@AllArgsConstructor
public class FileDownloadService {
    private final ProjectRetrievalService projectRetrievalService;

    public List<File> downloadProjectFiles(ProjectVersion projectVersion, String fileType) throws Exception {
        Project project = projectVersion.getProject();
        ProjectAppEntity projectAppEntity =
            this.projectRetrievalService.getProjectAppEntity(projectVersion);
        List<File> projectFiles = new ArrayList<>();

        ProjectEntities projectEntityMaps = new ProjectEntities(projectAppEntity);
        List<TimArtifactDefinition> artifactFiles = writeArtifactFiles(fileType, project, projectEntityMaps,
            projectFiles);
        List<TimTraceDefinition> traceFiles = writeTraceFiles(fileType, project, projectFiles,
            projectAppEntity,
            projectEntityMaps);
        TimSchema timData = new TimSchema(artifactFiles, traceFiles);
        File timFile = writeTimFile(project, timData);
        projectFiles.add(timFile);
        return projectFiles;
    }

    private List<TimTraceDefinition> writeTraceFiles(String fileType, Project project, List<File> projectFiles,
                                                     ProjectAppEntity projectAppEntity,
                                                     ProjectEntities projectEntityMaps) throws Exception {

        Type2TraceMap type2TraceMap = new Type2TraceMap(projectAppEntity, projectEntityMaps);
        List<TimTraceDefinition> traceFiles = new ArrayList<>();
        for (String sourceType : type2TraceMap.getSourceTypes()) {
            for (String targetType : type2TraceMap.getTargetTypes(sourceType)) {
                // Step - Create file
                String fileName = String.format("%s2%s.%s", sourceType, targetType, fileType);
                String pathToFile = ProjectPaths.Storage.getPathToProjectFile(project, fileName);
                File traceFileOutput = new File(pathToFile);

                // Step - Create trace file
                List<TraceAppEntity> traces = type2TraceMap.getTracesBetweenTypes(sourceType, targetType);
                AbstractTraceFile<?> traceFile = DataFileBuilder.createTraceFileParser(pathToFile, traces);
                TimTraceDefinition traceFileIdentifier
                    = new TimTraceDefinition(sourceType, targetType, fileName, false);
                traceFiles.add(traceFileIdentifier);
                traceFile.export(traceFileOutput);

                projectFiles.add(traceFileOutput);
            }
        }
        return traceFiles;
    }

    private List<TimArtifactDefinition> writeArtifactFiles(String fileType,
                                                            Project project,
                                                            ProjectEntities projectEntityMaps,
                                                            List<File> projectFiles) throws Exception {
        List<TimArtifactDefinition> artifactFiles = new ArrayList<>();
        for (String artifactType : projectEntityMaps.getArtifactTypes()) {
            String fileName = String.format("%s.%s", artifactType, fileType);
            String pathToFile = ProjectPaths.Storage.getPathToProjectFile(project, fileName);

            File artifactFileOutput = new File(pathToFile);
            List<ArtifactAppEntity> artifacts = projectEntityMaps.getArtifactsInType(artifactType);
            DocumentType documentType = getDocumentTypeFromType(artifactType);
            AbstractArtifactFile<?> artifactFile = DataFileBuilder.createArtifactFileParser(artifactType,
                pathToFile,
                documentType,
                artifacts);
            TimArtifactDefinition artifactFileIdentifier = new TimArtifactDefinition(artifactType, fileName);
            artifactFiles.add(artifactFileIdentifier);
            artifactFile.export(artifactFileOutput);
            projectFiles.add(artifactFileOutput);
        }
        return artifactFiles;
    }

    private DocumentType getDocumentTypeFromType(String artifactType) {
        List<Pair<DocumentType, Class<? extends Enum<?>>>> documentValues = new ArrayList<>();
        documentValues.add(new Pair<>(DocumentType.SAFETY_CASE, SafetyCaseType.class));
        documentValues.add(new Pair<>(DocumentType.FTA, FTAType.class));

        for (Pair<DocumentType, Class<? extends Enum<?>>> documentTypeClassPair : documentValues) {
            Class<? extends Enum<?>> enumClass = documentTypeClassPair.getValue1();
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

    private File writeTimFile(Project project, TimSchema timData) throws IOException {
        String pathToFile = ProjectPaths.Storage.getPathToProjectFile(project, ProjectVariables.TIM_FILENAME);
        File timFile = new File(pathToFile);
        new ObjectMapper().writeValue(timFile, timData);
        return timFile;
    }
}
