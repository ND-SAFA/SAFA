package edu.nd.crc.safa.test.services.builders;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

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
        this.withArtifact(artifactName, typeName);
        return this;
    }

    public ProjectBuilder withArtifact(String artifactName,
                                       String typeName) {
        getOrCreateType(typeName);
        this.dbEntityBuilder
            .newArtifact(projectName, typeName, artifactName)
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

    public ArtifactType getOrCreateType(String artifactType) {
        Map<String, ArtifactType> projectTypes = this.dbEntityBuilder
            .artifactTypes
            .get(this.projectName);
        return projectTypes.containsKey(artifactType)
            ? projectTypes.get(artifactType) :
            this.dbEntityBuilder.newTypeAndReturn(projectName, artifactType);
    }

    public ProjectBuilder withVersion() {
        ProjectVersion projectVersion = this.dbEntityBuilder.newVersionWithReturn(this.projectName);
        this.currentVersion.setNewVersion(projectVersion);
        return this;
    }

    public String getNextArtifactName(String typeName) {
        ArtifactType artifactType = getOrCreateType(typeName);
        String prefix = String.valueOf(artifactType.getName().toUpperCase().charAt(0));

        int nArtifactsInType = (int) this.artifactVersions
            .stream()
            .filter(a -> a.getArtifact().getType().getName().equals(artifactType.getName()))
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
