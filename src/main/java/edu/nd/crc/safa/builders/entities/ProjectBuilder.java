package edu.nd.crc.safa.builders.entities;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;

import edu.nd.crc.safa.server.entities.app.project.FTAType;
import edu.nd.crc.safa.server.entities.app.project.SafetyCaseType;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Builds project containing artifacts and trace links
 */
@Data
public class ProjectBuilder {
    public static final int DEFAULT_LENGTH = 50;
    static Random random = new Random();
    DbEntityBuilder dbEntityBuilder;
    String projectName;
    Project project;
    CurrentVersion currentVersion;
    List<ProjectVersion> projectVersions;
    List<Document> documents;
    List<Artifact> artifacts;
    List<ArtifactVersion> artifactVersions;

    public ProjectBuilder(DbEntityBuilder dbEntityBuilder, String projectName) {
        this.projectName = projectName;
        this.dbEntityBuilder = dbEntityBuilder;
        this.project = dbEntityBuilder.newProjectWithReturn(projectName);
        this.currentVersion = new CurrentVersion(0, dbEntityBuilder.newVersionWithReturn(projectName));
        this.projectVersions = this.currentVersion.asProjectVersions();
        this.documents = new ArrayList<>();
        this.artifacts = new ArrayList<>();
        this.artifactVersions = new ArrayList<>();
    }

    public static ProjectBuilder withProject(String projectName) {
        return new ProjectBuilder(DbEntityBuilder.getInstance(), projectName);
    }

    public static String generateText() {
        return ProjectBuilder.generateText(DEFAULT_LENGTH);
    }

    public static String generateText(int targetStringLength) {
        int leftLimit = 97; // letter 'a'
        int rightLimit = 122; // letter 'z'

        return ProjectBuilder
            .random
            .ints(leftLimit, rightLimit + 1)
            .limit(targetStringLength)
            .collect(StringBuilder::new, StringBuilder::appendCodePoint, StringBuilder::append)
            .toString();
    }

    public ProjectBuilder withArtifact(String typeName) {
        getOrCreateType(typeName);
        String artifactName = this.getNextArtifactName(typeName);
        this.withArtifact(artifactName, typeName, DocumentType.ARTIFACT_TREE);
        return this;
    }

    public ProjectBuilder withArtifact(String artifactName,
                                       String typeName,
                                       DocumentType documentType) {
        getOrCreateType(typeName);
        this.dbEntityBuilder
            .newArtifact(projectName, typeName, artifactName, documentType)
            .newArtifactBodyWithReturn(
                this.projectName,
                this.currentVersion.getVersionIndex(),
                ModificationType.ADDED,
                artifactName,
                ProjectBuilder.generateText(),
                ProjectBuilder.generateText()
            );
        return this;
    }

    public ProjectBuilder withFtaArtifact(FTAType ftaType) {
        String typeName = ftaType.toString();
        String artifactName = this.getNextArtifactName(typeName);
        this.withArtifact(artifactName, typeName, DocumentType.FTA);
        Artifact artifact = this.dbEntityBuilder.getArtifact(projectName, artifactName);
        this.dbEntityBuilder
            .newFtaArtifact(artifact, DocumentType.FTA, ftaType);
        return this;
    }

    public ProjectBuilder withSafetyArtifact(SafetyCaseType safetyCaseType) {
        String typeName = safetyCaseType.toString();
        String artifactName = this.getNextArtifactName(typeName);
        this.withArtifact(artifactName, typeName, DocumentType.SAFETY_CASE);
        Artifact artifact = this.dbEntityBuilder.getArtifact(projectName, artifactName);
        this.dbEntityBuilder
            .newSafetyArtifact(artifact, DocumentType.SAFETY_CASE, safetyCaseType);
        return this;
    }

    public ArtifactType getOrCreateType(String artifactType) {
        Map<String, ArtifactType> projectTypes = this.dbEntityBuilder
            .artifactTypes
            .get(this.projectName);
        return projectTypes.containsKey(artifactType)
            ? projectTypes.get(artifactType) :
            this.dbEntityBuilder.newTypeAndReturn(projectName, artifactType);
    }

    public ProjectVersion withVersion() {
        ProjectVersion projectVersion = this.dbEntityBuilder.newVersionWithReturn(this.projectName);
        this.currentVersion.setNewVersion(projectVersion);
        return projectVersion;
    }

    public String getNextArtifactName(String typeName) {
        ArtifactType artifactType = getOrCreateType(typeName);
        String prefix = "" + artifactType.getName().toUpperCase().charAt(0);

        int nArtifactsInType = (int) this.artifactVersions
            .stream()
            .filter(a -> a.getArtifact().getType().getName().equals(artifactType))
            .count();
        return String.format("%s%s", prefix, nArtifactsInType);
    }

    @Data
    @AllArgsConstructor
    public static class CurrentVersion {
        int versionIndex;
        ProjectVersion projectVersion;

        List<ProjectVersion> asProjectVersions() {
            return new ArrayList<>(List.of(this.projectVersion));
        }

        public void setNewVersion(ProjectVersion projectVersion) {
            this.versionIndex++;
            this.projectVersion = projectVersion;
        }
    }
}
