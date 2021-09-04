package edu.nd.crc.safa.db.entities.builders;

import java.util.Hashtable;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.db.entities.sql.ModificationType;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.repositories.sql.ArtifactBodyRepository;
import edu.nd.crc.safa.db.repositories.sql.ArtifactRepository;
import edu.nd.crc.safa.db.repositories.sql.ArtifactTypeRepository;
import edu.nd.crc.safa.db.repositories.sql.ProjectRepository;
import edu.nd.crc.safa.db.repositories.sql.ProjectVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * The following class is a helper for the unit tests so that entities
 * and verifications can be human readable and repeatable
 */
@Component
public class EntityBuilder extends BaseBuilder {

    ProjectRepository projectRepository;
    ProjectVersionRepository projectVersionRepository;
    ArtifactTypeRepository artifactTypeRepository;
    ArtifactRepository artifactRepository;
    ArtifactBodyRepository artifactBodyRepository;

    Hashtable<String, Project> projects;
    Hashtable<String, Hashtable<Integer, ProjectVersion>> projectVersions;
    Hashtable<String, Hashtable<String, ArtifactType>> artifactTypes;
    Hashtable<String, Hashtable<String, Artifact>> artifacts;
    Hashtable<String, Hashtable<String, Hashtable<Long, ArtifactBody>>> bodies;

    @Autowired
    public EntityBuilder(ProjectRepository projectRepository,
                         ProjectVersionRepository projectVersionRepository,
                         ArtifactTypeRepository artifactTypeRepository,
                         ArtifactRepository artifactRepository,
                         ArtifactBodyRepository artifactBodyRepository) {
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.artifactRepository = artifactRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        createEmptyData();
    }

    public void createEmptyData() {
        this.projects = new Hashtable<>();
        this.projectVersions = new Hashtable<>();
        this.artifactTypes = new Hashtable<>();
        this.artifacts = new Hashtable<>();
        this.bodies = new Hashtable<>();
        this.projectRepository.deleteAll();
        this.projectVersionRepository.deleteAll();
        this.artifactTypeRepository.deleteAll();
        this.artifactRepository.deleteAll();
        this.artifactBodyRepository.deleteAll();
    }

    public Project newProjectWithReturn(String name) {
        return this.newProject(name).getProject(name);
    }

    public EntityBuilder newProject(String name) {
        Project project = new Project(name);
        this.projectRepository.save(project);
        this.projects.put(name, project);
        return this;
    }

    public ProjectVersion newVersionWithReturn(String projectName) {
        this.newVersion(projectName);
        int versionIndex = this.projectVersions.get(projectName).size() - 1;
        return this.getProjectVersion(projectName, versionIndex);
    }

    public EntityBuilder newVersion(String projectName) {
        Project project = this.projects.get(projectName);
        ProjectVersion projectVersion = new ProjectVersion(project);
        this.projectVersionRepository.save(projectVersion);
        addEntry(this.projectVersions, projectName, projectVersion);
        return this;
    }

    public ArtifactType newTypeAndReturn(String projectName, String typeName) {
        return this.newType(projectName, typeName).getType(projectName, typeName);
    }

    public EntityBuilder newType(String projectName, String typeName) {
        Project project = this.projects.get(projectName);
        ArtifactType artifactType = new ArtifactType(project, typeName);
        this.artifactTypeRepository.save(artifactType);
        addEntry(this.artifactTypes, projectName, typeName, artifactType);
        return this;
    }

    public Artifact newArtifactWithReturn(String projectName, String typeName, String artifactName) {
        return this.newArtifact(projectName, typeName, artifactName).getArtifact(projectName, artifactName);
    }

    public EntityBuilder newArtifact(String projectName, String typeName, String artifactName) {
        Project project = this.projects.get(projectName);
        ArtifactType artifactType = this.artifactTypes.get(projectName).get(typeName);
        Artifact artifact = new Artifact(project, artifactType, artifactName);
        this.artifactRepository.save(artifact);
        this.addEntry(this.artifacts, projectName, artifactName, artifact);
        return this;
    }

    public EntityBuilder newArtifactAndBody(String projectName,
                                            String typeName,
                                            String artifactName,
                                            String summary,
                                            String content) {
        return newArtifactAndBody(projectName, 0, typeName, artifactName, summary, content);
    }

    public EntityBuilder newArtifactAndBody(String projectName,
                                            int versionIndex,
                                            String typeName,
                                            String artifactName,
                                            String summary,
                                            String content) {
        newArtifact(projectName, typeName, artifactName)
            .getArtifact(projectName, artifactName);
        return this.newArtifactBody(projectName, versionIndex, artifactName, summary, content);
    }

    public EntityBuilder newArtifactBody(String projectName,
                                         String artifactName,
                                         String summary,
                                         String content) {
        return newArtifactBody(projectName, 0, artifactName, summary, content);
    }

    public EntityBuilder newArtifactBody(String projectName,
                                         int versionIndex,
                                         String artifactName,
                                         String summary,
                                         String content) {
        return newArtifactBody(projectName, versionIndex, ModificationType.ADDED, artifactName, summary, content);
    }

    public ArtifactBody newArtifactBodyWithReturn(String projectName,
                                                  int versionIndex,
                                                  ModificationType modificationType,
                                                  String artifactName,
                                                  String summary,
                                                  String content) {
        newArtifactBody(projectName, versionIndex, modificationType, artifactName, summary, content);
        return getArtifactBody(projectName, artifactName, (long) versionIndex);
    }

    public EntityBuilder newArtifactBody(String projectName,
                                         int versionIndex,
                                         ModificationType modificationType,
                                         String artifactName,
                                         String summary,
                                         String content) {
        ProjectVersion projectVersion = this.getProjectVersion(projectName, versionIndex);
        Artifact artifact = this.getArtifact(projectName, artifactName);
        ArtifactBody artifactBody = new ArtifactBody(projectVersion,
            modificationType,
            artifact,
            summary,
            content);
        this.artifactBodyRepository.save(artifactBody);
        addArtifactBody(bodies, projectName, artifactName, projectVersion.getVersionId(), artifactBody);
        return this;
    }

    public EntityBuilder updateProjectName(String currentName, String newName) {
        Project project = this.projects.get(currentName);
        project.setName(newName);
        this.projectRepository.save(project);
        return this;
    }

    public EntityBuilder updateTypeName(String projectName, String currentName, String newName) {
        ArtifactType artifactType = this.artifactTypes.get(projectName).get(currentName);
        artifactType.setName(newName);
        this.artifactTypeRepository.save(artifactType);
        return this;
    }

    public EntityBuilder updateArtifactName(String projectName, String artifactName, String newName) {
        Artifact artifact = this.artifacts.get(projectName).get(artifactName);
        artifact.setName(newName);
        this.artifactRepository.save(artifact);
        return this;
    }

    public Project getProject(String projectName) {
        return this.projects.get(projectName);
    }

    public ProjectVersion getProjectVersion(String projectName, int index) {
        return this.projectVersions.get(projectName).get(index);
    }

    public Artifact getArtifact(String projectName, String artifactName) {
        return this.artifacts.get(projectName).get(artifactName);
    }

    public List<Artifact> getArtifacts(String projectName) {
        return this.artifacts.get(projectName).values().stream().collect(Collectors.toList());
    }

    public ArtifactBody getArtifactBody(String projectName, String artifactName, Long versionIndex) {
        return this.bodies.get(projectName).get(artifactName).get(versionIndex);
    }

    public ArtifactType getType(String projectName, String typeName) {
        return this.artifactTypes.get(projectName).get(typeName);
    }
}
