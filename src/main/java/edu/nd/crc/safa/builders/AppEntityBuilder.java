package edu.nd.crc.safa.builders;

import java.util.Hashtable;

import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;

import org.springframework.stereotype.Component;

@Component
public class AppEntityBuilder extends BaseBuilder {

    Hashtable<String, ProjectAppEntity> projects;
    Hashtable<String, Hashtable<String, ArtifactAppEntity>> artifacts;

    public AppEntityBuilder() {
        createEmptyData();
    }

    public void createEmptyData() {
        projects = new Hashtable<>();
        artifacts = new Hashtable<>();
    }

    public AppEntityBuilder withProject(String name) {
        ProjectAppEntity project = new ProjectAppEntity();
        this.projects.put(name, project);
        return this;
    }

    public AppEntityBuilder withArtifact(String projectName, String artifactName) {
        ProjectAppEntity project = projects.get(projectName);
        ArtifactAppEntity artifact = new ArtifactAppEntity();
        artifact.setName(artifactName);
        addEntry(artifacts, projectName, artifactName, artifact);
        project.addArtifact(artifact);
        return this;
    }

    public ProjectAppEntity getProject(String projectName) {
        return this.projects.get(projectName);
    }
}
