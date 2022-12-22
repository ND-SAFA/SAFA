package builders;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactFieldType;
import edu.nd.crc.safa.features.artifacts.entities.FTAType;
import edu.nd.crc.safa.features.artifacts.entities.SafetyCaseType;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.CustomAttribute;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.features.artifacts.repositories.schema.CustomAttributeRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.ArtifactVersionRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.ArtifactVersionRepositoryImpl;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.memberships.repositories.ProjectMembershipRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkRepository;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.types.ArtifactType;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;

import org.junit.jupiter.api.AfterEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Provides an API for quickly creating persistent entities in a project.
 */
@Component
public class DbEntityBuilder extends AbstractBuilder {

    static final int MAJOR_VERSION = 1;
    static final int MINOR_VERSION = 1;
    static DbEntityBuilder instance;
    private final ProjectRepository projectRepository;
    private final ProjectVersionRepository projectVersionRepository;
    private final DocumentRepository documentRepository;
    private final DocumentArtifactRepository documentArtifactRepository;
    private final ArtifactTypeRepository artifactTypeRepository;
    private final ArtifactRepository artifactRepository;
    private final ArtifactVersionRepository artifactVersionRepository;
    private final TraceLinkRepository traceLinkRepository;
    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final ProjectMembershipRepository projectMembershipRepository;
    private final ArtifactVersionRepositoryImpl artifactVersionRepositoryImpl;
    private final ProjectService projectService;
    private final CustomAttributeRepository customAttributeRepository;
    Map<String, Project> projects;
    Map<String, Map<Integer, ProjectVersion>> versions;
    Map<String, Map<String, Document>> documents;
    Map<String, Map<String, ArtifactType>> artifactTypes;
    Map<String, Map<String, Artifact>> artifacts;
    Map<String, Map<String, Map<Long, ArtifactVersion>>> bodies;
    int revisionNumber;
    SafaUser currentUser;

    @Autowired
    public DbEntityBuilder(ServiceProvider serviceProvider) {
        this.projectRepository = serviceProvider.getProjectRepository();
        this.projectService = serviceProvider.getProjectService();
        this.projectVersionRepository = serviceProvider.getProjectVersionRepository();
        this.documentRepository = serviceProvider.getDocumentRepository();
        this.documentArtifactRepository = serviceProvider.getDocumentArtifactRepository();
        this.artifactTypeRepository = serviceProvider.getArtifactTypeRepository();
        this.artifactRepository = serviceProvider.getArtifactRepository();
        this.artifactVersionRepository = serviceProvider.getArtifactVersionRepository();
        this.traceLinkRepository = serviceProvider.getTraceLinkRepository();
        this.traceLinkVersionRepository = serviceProvider.getTraceLinkVersionRepository();
        this.projectMembershipRepository = serviceProvider.getProjectMembershipRepository();
        this.artifactVersionRepositoryImpl = serviceProvider.getArtifactVersionRepositoryImpl();
        this.customAttributeRepository = serviceProvider.getCustomAttributeRepository();
        DbEntityBuilder.instance = this;
    }

    public static DbEntityBuilder getInstance() {
        return DbEntityBuilder.instance;
    }

    public void createEmptyData() throws IOException {
        this.projects = new Hashtable<>();
        this.versions = new Hashtable<>();
        this.documents = new Hashtable<>();
        this.artifactTypes = new Hashtable<>();
        this.artifacts = new Hashtable<>();
        this.bodies = new Hashtable<>();

        this.deleteProjectFiles();
        this.projectRepository.deleteAll();
        this.projectVersionRepository.deleteAll();
        this.documentRepository.deleteAll();
        this.documentArtifactRepository.deleteAll();
        this.artifactTypeRepository.deleteAll();
        this.artifactRepository.deleteAll();
        this.artifactVersionRepository.deleteAll();
        this.customAttributeRepository.deleteAll();
        this.revisionNumber = 1;
    }

    @AfterEach
    public void deleteProjectFiles() throws IOException {
        //Deletes project data
        for (Project project : this.projectRepository.findAll()) {
            projectService.deleteProject(project);
        }
        projectRepository.deleteAll();
    }

    public void setCurrentUser(SafaUser user) {
        this.currentUser = user;
    }

    public Project newProjectWithReturn(String name) {
        return this.newProject(name).getProject(name);
    }

    public DbEntityBuilder newProject(String name) {
        return newProject(name, currentUser);
    }

    public DbEntityBuilder newProject(String name, SafaUser owner) {
        Project project = new Project(name, "");
        this.projectRepository.save(project);
        this.projectMembershipRepository.save(new ProjectMembership(project, owner, ProjectRole.OWNER));
        this.projects.put(name, project);
        this.versions.put(name, new Hashtable<>());
        this.artifactTypes.put(name, new Hashtable<>());
        this.artifacts.put(name, new Hashtable<>());
        this.bodies.put(name, new Hashtable<>());
        return this;
    }

    public boolean hasDocument(String projectName,
                               String documentName) {
        assertProjectExists(this.documents, projectName);
        return this.documents.get(projectName).containsKey(documentName);
    }

    public DbEntityBuilder newDocument(String projectName,
                                       String docName,
                                       String docDescription,
                                       DocumentType docType) {
        Project project = this.getProject(projectName);
        Document document = new Document(null, project, docType, docName, docDescription);
        this.documentRepository.save(document);
        addEntry(this.documents, projectName, docName, document);
        return this;
    }

    public DbEntityBuilder newDocumentArtifact(String projectName,
                                               int versionIndex,
                                               String docName,
                                               String artifactName) {
        ProjectVersion projectVersion = this.getProjectVersion(projectName, versionIndex);
        Document document = this.getDocument(projectName, docName);
        Artifact artifact = this.getArtifact(projectName, artifactName);
        DocumentArtifact documentArtifact = new DocumentArtifact(projectVersion, document, artifact);
        this.documentArtifactRepository.save(documentArtifact);
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
            MAJOR_VERSION,
            MINOR_VERSION,
            this.revisionNumber++);
        this.projectVersionRepository.save(projectVersion);
        addEntry(this.versions, projectName, projectVersion);
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

    public boolean hasType(String projectName, String typeName) {
        assertProjectExists(this.artifactTypes, projectName);
        return this.artifactTypes.get(projectName).containsKey(typeName);
    }

    public DbEntityBuilder newCustomAttribute(String projectName, ArtifactFieldType type, String label, String key) {
        newCustomAttributeWithReturn(projectName, type, label, key);
        return this;
    }

    public CustomAttribute newCustomAttributeWithReturn(String projectName, ArtifactFieldType type, String label, String key) {
        Project project = getProject(projectName);
        CustomAttribute field = new CustomAttribute();
        field.setProject(project);
        field.setType(type);
        field.setLabel(label);
        field.setKeyname(key);
        return this.customAttributeRepository.save(field);
    }

    public Artifact newArtifactWithReturn(String projectName, String typeName, String artifactName) {
        return this.newArtifact(projectName, typeName, artifactName).getArtifact(projectName, artifactName);
    }

    public DbEntityBuilder newArtifact(String projectName,
                                       String typeName,
                                       String artifactName) {
        return newArtifact(projectName, typeName, artifactName, DocumentType.ARTIFACT_TREE);
    }

    public DbEntityBuilder newArtifact(String projectName,
                                       String typeName,
                                       String artifactName,
                                       DocumentType documentType) {
        Project project = getProject(projectName);
        ArtifactType artifactType = getType(projectName, typeName);
        Artifact artifact = new Artifact(project, artifactType, artifactName, documentType);
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

    public ArtifactVersion newArtifactBodyWithReturn(String projectName,
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
        ArtifactVersion artifactVersion = new ArtifactVersion(projectVersion,
            modificationType,
            artifact,
            summary,
            content);
        this.artifactVersionRepository.save(artifactVersion);
        addArtifactBody(bodies, projectName, artifactName, versionIndex, artifactVersion);
        return this;
    }

    public DbEntityBuilder newTraceLink(String projectName,
                                        String sourceName,
                                        String targetName,
                                        int projectVersionIndex) {
        Artifact source = this.getArtifact(projectName, sourceName);
        Artifact target = this.getArtifact(projectName, targetName);
        TraceLink traceLink = new TraceLink(source, target);
        this.traceLinkRepository.save(traceLink);
        ProjectVersion projectVersion = this.getProjectVersion(projectName, projectVersionIndex);
        TraceLinkVersion traceLinkVersion = (new TraceLinkVersion())
            .withProjectVersion(projectVersion)
            .withTraceLink(traceLink)
            .withModificationType(ModificationType.REMOVED)
            .withManualTraceType();
        traceLinkVersion.setApprovalStatus(ApprovalStatus.APPROVED);
        this.traceLinkVersionRepository.save(traceLinkVersion);
        return this;
    }

    public DbEntityBuilder newGeneratedTraceLink(String projectName,
                                                 String sourceName,
                                                 String targetName,
                                                 double score,
                                                 int projectVersionIndex) {
        Artifact source = this.getArtifact(projectName, sourceName);
        Artifact target = this.getArtifact(projectName, targetName);
        TraceLink traceLink = new TraceLink(source, target);
        this.traceLinkRepository.save(traceLink);
        ProjectVersion projectVersion = this.getProjectVersion(projectName, projectVersionIndex);
        TraceLinkVersion traceLinkVersion = TraceLinkVersion.createGeneratedLinkWithVersionAndModification(
            projectVersion,
            ModificationType.ADDED,
            traceLink,
            score
        );
        this.traceLinkVersionRepository.save(traceLinkVersion);
        return this;
    }

    public DbEntityBuilder newFtaArtifact(Artifact artifact,
                                          DocumentType documentType,
                                          FTAType ftaType
    ) {
        ArtifactAppEntity artifactAppEntity = new ArtifactAppEntity();
        artifactAppEntity.setDocumentType(documentType);
        artifactAppEntity.setLogicType(ftaType);
        artifactVersionRepositoryImpl.createOrUpdateDocumentNodeInformation(
            artifactAppEntity,
            artifact
        );
        return this;
    }

    public DbEntityBuilder newSafetyArtifact(Artifact artifact,
                                             DocumentType documentType,
                                             SafetyCaseType safetyCaseType
    ) {
        ArtifactAppEntity artifactAppEntity = new ArtifactAppEntity();
        artifactAppEntity.setDocumentType(documentType);
        artifactAppEntity.setSafetyCaseType(safetyCaseType);
        artifactVersionRepositoryImpl.createOrUpdateDocumentNodeInformation(
            artifactAppEntity,
            artifact
        );
        return this;
    }

    public Project getProject(String projectName) {
        assertProjectExists(this.projects, projectName);
        return this.projects.get(projectName);
    }

    public ProjectVersion getProjectVersion(String projectName, int versionIndex) {
        assertProjectExists(this.versions, projectName);
        assertEntityExists(this.versions.get(projectName), versionIndex, "Project index");
        return this.versions.get(projectName).get(versionIndex);
    }

    public Document getDocument(String projectName, String docName) {
        assertProjectExists(this.documents, projectName);
        assertEntityExists(this.documents.get(projectName), docName, "Document");
        return this.documents.get(projectName).get(docName);
    }

    public List<ProjectVersion> getProjectVersions(String projectName) {
        assertProjectExists(this.versions, projectName);
        return new ArrayList<>(this.versions.get(projectName).values());
    }

    public Artifact getArtifact(String projectName, String artifactName) {
        assertProjectExists(this.artifacts, projectName);
        if (!this.artifacts.get(projectName).containsKey(artifactName)) {
            throw new SafaError("Artifact %s has not been created.", artifactName);
        }
        return this.artifacts.get(projectName).get(artifactName);
    }

    public List<Artifact> getArtifacts(String projectName) {
        assertProjectExists(this.artifacts, projectName);
        return new ArrayList<>(this.artifacts.get(projectName).values());
    }

    public ArtifactVersion getArtifactBody(String projectName, String artifactName, int versionIndex) {
        assertProjectExists(this.bodies, projectName);
        Map<String, Map<Long, ArtifactVersion>> project = this.bodies.get(projectName);
        assertEntityExists(project, artifactName, "Artifact");
        assertEntityExists(project.get(artifactName), (long) versionIndex, "Version Index");
        return this.bodies.get(projectName).get(artifactName).get((long) versionIndex);
    }

    public List<ArtifactVersion> getArtifactBodies(String projectName) {
        assertProjectExists(this.bodies, projectName);
        List<ArtifactVersion> projectBodies = new ArrayList<>();
        this.bodies.get(projectName).values().forEach(artifactVersionTable ->
            projectBodies.addAll(artifactVersionTable.values()));
        return projectBodies;
    }

    public ArtifactType getType(String projectName, String typeName) {
        assertProjectExists(this.artifactTypes, projectName);
        assertEntityExists(this.artifactTypes.get(projectName), typeName, "ArtifactType");
        return this.artifactTypes.get(projectName).get(typeName);
    }

    public List<TraceLinkVersion> getTraceLinks(String projectName) {
        Project project = getProject(projectName);
        return this.traceLinkVersionRepository.getProjectLinks(project);
    }

    private <T> void assertProjectExists(Map<String, T> table, String projectName) {
        assertEntityExists(table, projectName, "Project");
    }

    /**
     * Asserts that the given table has specified keyName. Otherwise, an error is thrown signalling that
     * given entityName is missing.
     *
     * @param table      The table containing the records to check
     * @param keyName    The name of the key to check the table for.
     * @param entityName The name of the entity to print if the key is missing.
     * @param <T>        The value of the table.
     * @param <K>        The Type of Key used to index into the table.
     */
    private <T, K> void assertEntityExists(Map<K, T> table, K keyName, String entityName) {
        if (!table.containsKey(keyName)) {
            throw new IllegalStateException(String.format("[%s: %s] has not been created.", keyName, entityName));
        }
    }
}
