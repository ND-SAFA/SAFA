package edu.nd.crc.safa.builders;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Provides an API for quickly creating entities in a project.
 */
@Component
public class DbEntityBuilder extends BaseBuilder {

    final int majorVersion = 1;
    final int minorVersion = 1;

    ProjectRepository projectRepository;
    ProjectVersionRepository projectVersionRepository;
    ArtifactTypeRepository artifactTypeRepository;
    ArtifactRepository artifactRepository;
    ArtifactBodyRepository artifactBodyRepository;
    TraceLinkRepository traceLinkRepository;

    Hashtable<String, Project> projects;
    Hashtable<String, Hashtable<Integer, ProjectVersion>> projectVersions;
    Hashtable<String, Hashtable<String, ArtifactType>> artifactTypes;
    Hashtable<String, Hashtable<String, Artifact>> artifacts;
    Hashtable<String, Hashtable<String, Hashtable<Long, ArtifactBody>>> bodies;

    int revisionNumber;

    @Autowired
    public DbEntityBuilder(ProjectRepository projectRepository,
                           ProjectVersionRepository projectVersionRepository,
                           ArtifactTypeRepository artifactTypeRepository,
                           ArtifactRepository artifactRepository,
                           ArtifactBodyRepository artifactBodyRepository,
                           TraceLinkRepository traceLinkRepository) {
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.artifactRepository = artifactRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.traceLinkRepository = traceLinkRepository;
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
        this.revisionNumber = 1;
    }

    public Project newProjectWithReturn(String name) {
        return this.newProject(name).getProject(name);
    }

    public DbEntityBuilder newProject(String name) {
        Project project = new Project(name, "");
        this.projectRepository.save(project);
        this.projects.put(name, project);
        this.projectVersions.put(name, new Hashtable<>());
        this.artifactTypes.put(name, new Hashtable<>());
        this.artifacts.put(name, new Hashtable<>());
        this.bodies.put(name, new Hashtable<>());
        return this;
    }

    public ProjectVersion newVersionWithReturn(String projectName) {
        this.newVersion(projectName);
        int versionIndex = getProjectVersions(projectName).size() - 1;
        return this.getProjectVersion(projectName, versionIndex);
    }

    public DbEntityBuilder newVersion(String projectName) {
        Project project = getProject(projectName);
        ProjectVersion projectVersion = new ProjectVersion(project,
            this.majorVersion,
            this.minorVersion,
            this.revisionNumber++);
        this.projectVersionRepository.save(projectVersion);
        addEntry(this.projectVersions, projectName, projectVersion);
        return this;
    }

    public ArtifactType newTypeAndReturn(String projectName, String typeName) {
        return this.newType(projectName, typeName).getType(projectName, typeName);
    }

    public DbEntityBuilder newType(String projectName, String typeName) {
        Project project = getProject(projectName);
        ArtifactType artifactType = new ArtifactType(project, typeName);
        this.artifactTypeRepository.save(artifactType);
        addEntry(this.artifactTypes, projectName, typeName, artifactType);
        return this;
    }

    public Artifact newArtifactWithReturn(String projectName, String typeName, String artifactName) {
        return this.newArtifact(projectName, typeName, artifactName).getArtifact(projectName, artifactName);
    }

    public DbEntityBuilder newArtifact(String projectName, String typeName, String artifactName) {
        Project project = getProject(projectName);
        ArtifactType artifactType = getType(projectName, typeName);
        Artifact artifact = new Artifact(project, artifactType, artifactName);
        this.artifactRepository.save(artifact);
        this.addEntry(this.artifacts, projectName, artifactName, artifact);
        return this;
    }

    public DbEntityBuilder newArtifactAndBody(String projectName,
                                              String typeName,
                                              String artifactName,
                                              String summary,
                                              String content) {
        return newArtifactAndBody(projectName, 0, typeName, artifactName, summary, content);
    }

    public DbEntityBuilder newArtifactAndBody(String projectName,
                                              int versionIndex,
                                              String typeName,
                                              String artifactName,
                                              String summary,
                                              String content) {
        newArtifact(projectName, typeName, artifactName)
            .getArtifact(projectName, artifactName);
        return this.newArtifactBody(projectName, versionIndex, artifactName, summary, content);
    }

    public ArtifactBody newArtifactBodyWithReturn(String projectName,
                                                  int versionIndex,
                                                  ModificationType modificationType,
                                                  String artifactName,
                                                  String summary,
                                                  String content) {
        newArtifactBody(projectName, versionIndex, modificationType, artifactName, summary, content);
        return getArtifactBody(projectName, artifactName, versionIndex);
    }

    public DbEntityBuilder newArtifactBody(String projectName,
                                           String artifactName,
                                           String summary,
                                           String content) {
        return newArtifactBody(projectName, 0, artifactName, summary, content);
    }

    public DbEntityBuilder newArtifactBody(String projectName,
                                           int versionIndex,
                                           String artifactName,
                                           String summary,
                                           String content) {
        return newArtifactBody(projectName, versionIndex, ModificationType.ADDED, artifactName, summary, content);
    }

    public DbEntityBuilder newArtifactBody(String projectName,
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
        addArtifactBody(bodies, projectName, artifactName, versionIndex, artifactBody);
        return this;
    }

    public DbEntityBuilder newTraceLink(String projectName, String sourceName, String targetName) {
        Artifact source = this.getArtifact(projectName, sourceName);
        Artifact target = this.getArtifact(projectName, targetName);
        TraceLink traceLink = new TraceLink(source, target);
        this.traceLinkRepository.save(traceLink);
        return this;
    }

    public DbEntityBuilder newGeneratedTraceLink(String projectName,
                                                 String sourceName,
                                                 String targetName,
                                                 double score) {
        Artifact source = this.getArtifact(projectName, sourceName);
        Artifact target = this.getArtifact(projectName, targetName);
        TraceLink traceLink = new TraceLink(source, target, 0.5);
        this.traceLinkRepository.save(traceLink);
        return this;
    }

    public DbEntityBuilder updateProjectName(String currentName, String newName) {
        Project project = getProject(currentName);
        project.setName(newName);
        this.projectRepository.save(project);
        return this;
    }

    public DbEntityBuilder updateTypeName(String projectName, String currentName, String newName) {
        ArtifactType artifactType = getType(projectName, currentName);
        artifactType.setName(newName);
        this.artifactTypeRepository.save(artifactType);
        return this;
    }

    public DbEntityBuilder updateArtifactName(String projectName, String artifactName, String newName) {
        Artifact artifact = getArtifact(projectName, artifactName);
        artifact.setName(newName);
        this.artifactRepository.save(artifact);
        return this;
    }

    public Project getProject(String projectName) {
        assertProjectExists(this.projects, projectName);
        return this.projects.get(projectName);
    }

    public ProjectVersion getProjectVersion(String projectName, int index) {
        assertProjectExists(this.projectVersions, projectName);
        assertEntityExists(this.projectVersions.get(projectName), "Project index", index);
        return this.projectVersions.get(projectName).get(index);
    }

    public List<ProjectVersion> getProjectVersions(String projectName) {
        assertProjectExists(this.projectVersions, projectName);
        return new ArrayList<>(this.projectVersions.get(projectName).values());
    }

    public Artifact getArtifact(String projectName, String artifactName) {
        assertProjectExists(this.artifacts, projectName);
        if (!this.artifacts.get(projectName).containsKey(artifactName)) {
            throw new RuntimeException(String.format("Artifact %s has not been created.", artifactName));
        }
        return this.artifacts.get(projectName).get(artifactName);
    }

    public List<Artifact> getArtifacts(String projectName) {
        assertProjectExists(this.artifacts, projectName);
        return new ArrayList<>(this.artifacts.get(projectName).values());
    }

    public ArtifactBody getArtifactBody(String projectName, String artifactName, int versionIndex) {
        assertProjectExists(this.bodies, projectName);
        Hashtable<String, Hashtable<Long, ArtifactBody>> project = this.bodies.get(projectName);
        assertEntityExists(project, "Artifact", artifactName);
        assertEntityExists(project.get(artifactName), "Version Index", (long) versionIndex);
        return this.bodies.get(projectName).get(artifactName).get((long) versionIndex);
    }

    public List<ArtifactBody> getArtifactBodies(String projectName) {
        assertProjectExists(this.bodies, projectName);
        List<ArtifactBody> projectBodies = new ArrayList<>();
        this.bodies.get(projectName).values().forEach(artifactVersionTable -> {
            projectBodies.addAll(artifactVersionTable.values());
        });
        return projectBodies;
    }

    public ArtifactType getType(String projectName, String typeName) {
        assertProjectExists(this.artifactTypes, projectName);
        assertEntityExists(this.artifactTypes.get(projectName), "ArtifactType", typeName);
        return this.artifactTypes.get(projectName).get(typeName);
    }

    public List<TraceLink> getTraceLinks(String projectName) {
        Project project = getProject(projectName);
        return this.traceLinkRepository.getLinks(project);
    }

    private <T> void assertProjectExists(Hashtable<String, T> table, String projectName) {
        assertEntityExists(table, "Project", projectName);
    }

    private <T, K> void assertEntityExists(Hashtable<K, T> table, String entityName, K keyName) {
        if (!table.containsKey(keyName)) {
            throw new RuntimeException(String.format("[%s: %s] has not been created.", keyName, entityName));
        }
    }
}
