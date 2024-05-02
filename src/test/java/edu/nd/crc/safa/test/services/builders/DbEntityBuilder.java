package edu.nd.crc.safa.test.services.builders;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepositoryImpl;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.repositories.definitions.CustomAttributeRepository;
import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.memberships.services.OrganizationMembershipService;
import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.memberships.services.TeamMembershipService;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.IRole;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.OrganizationRole;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.features.organizations.services.TeamService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkRepository;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.types.services.TypeService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.features.versions.services.VersionService;
import edu.nd.crc.safa.test.features.attributes.AttributesForTesting;

import org.junit.jupiter.api.AfterEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Provides an API for quickly creating persistent entities in a project.
 */
@Component
public class DbEntityBuilder extends AbstractBuilder {

    static final int MAJOR_VERSION = 1;
    static final int MINOR_VERSION = 0;
    static DbEntityBuilder instance;
    private final ProjectRepository projectRepository;
    private final ProjectVersionRepository projectVersionRepository;
    private final DocumentRepository documentRepository;
    private final DocumentArtifactRepository documentArtifactRepository;
    private final TypeService artifactTypeService;
    private final ArtifactRepository artifactRepository;
    private final ArtifactVersionRepository artifactVersionRepository;
    private final TraceLinkRepository traceLinkRepository;
    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final ProjectService projectService;
    private final CustomAttributeRepository customAttributeRepository;
    private final AttributeSystemServiceProvider attributeSystemServiceProvider;
    private final VersionService versionService;
    private final TeamService teamService;
    private final OrganizationService organizationService;
    private final TeamMembershipService teamMembershipService;
    private final OrganizationMembershipService organizationMembershipService;
    private final ProjectMembershipService projectMembershipService;

    Map<String, Project> projects;
    Map<String, Map<Integer, ProjectVersion>> versions;
    Map<String, Map<String, Document>> documents;
    Map<String, Map<String, ArtifactType>> artifactTypes;
    Map<String, Map<String, Artifact>> artifacts;
    Map<String, Map<String, Map<Long, ArtifactVersion>>> bodies;
    int revisionNumber;
    SafaUser currentUser;

    @Autowired
    public DbEntityBuilder(ServiceProvider serviceProvider,
                           CustomAttributeRepository customAttributeRepository,
                           AttributeSystemServiceProvider attributeSystemServiceProvider,
                           ArtifactVersionRepositoryImpl artifactVersionRepositoryImpl) {
        this.projects = new Hashtable<>();
        this.projectRepository = serviceProvider.getProjectRepository();
        this.projectService = serviceProvider.getProjectService();
        this.projectVersionRepository = serviceProvider.getProjectVersionRepository();
        this.documentRepository = serviceProvider.getDocumentRepository();
        this.documentArtifactRepository = serviceProvider.getDocumentArtifactRepository();
        this.artifactTypeService = serviceProvider.getTypeService();
        this.artifactRepository = serviceProvider.getArtifactRepository();
        this.artifactVersionRepository = serviceProvider.getArtifactVersionRepository();
        this.traceLinkRepository = serviceProvider.getTraceLinkRepository();
        this.traceLinkVersionRepository = serviceProvider.getTraceLinkVersionRepository();
        this.customAttributeRepository = customAttributeRepository;
        this.attributeSystemServiceProvider = attributeSystemServiceProvider;
        this.versionService = serviceProvider.getVersionService();
        this.teamService = serviceProvider.getTeamService();
        this.organizationService = serviceProvider.getOrganizationService();
        this.teamMembershipService = serviceProvider.getTeamMembershipService();
        this.organizationMembershipService = serviceProvider.getOrgMembershipService();
        this.projectMembershipService = serviceProvider.getProjectMembershipService();
        DbEntityBuilder.instance = this;
        this.initializeData();
    }

    public static DbEntityBuilder getInstance() {
        return DbEntityBuilder.instance;
    }

    public void initializeData() {
        try {
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
            this.artifactTypeService.deleteAll();
            this.artifactRepository.deleteAll();
            this.artifactVersionRepository.deleteAll();
            this.customAttributeRepository.deleteAll();
            this.revisionNumber = 0;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @AfterEach
    public void deleteProjectFiles() throws IOException {
        //Deletes project data
        for (Project project : this.projectRepository.findAll()) {
            projectService.deleteProject(null, project);
        }
        projectRepository.deleteAll();
    }

    public void setCurrentUser(SafaUser user) {
        this.currentUser = user;
    }

    public Project newProjectWithReturn(String name) {
        return newProjectWithReturn(name, currentUser);
    }

    public Project newProjectWithReturn(String name, SafaUser owner) {
        Project project = this.projectService.createProject(name, "", owner);
        createProjectTables(name, project);
        return project;
    }

    public Project newProjectWithReturn(String name, Team owner) {
        Project project = this.projectService.createProject(name, "", owner);
        createProjectTables(name, project);
        return project;
    }

    public DbEntityBuilder newProject(String name) {
        newProjectWithReturn(name);
        return this;
    }

    public DbEntityBuilder newProject(String name, SafaUser owner) {
        newProjectWithReturn(name, owner);
        return this;
    }

    public DbEntityBuilder newProject(String name, Team owner) {
        newProjectWithReturn(name, owner);
        return this;
    }

    private void createProjectTables(String name, Project project) {
        this.projects.put(name, project);
        this.versions.put(name, new Hashtable<>());
        this.artifactTypes.put(name, new Hashtable<>());
        this.artifacts.put(name, new Hashtable<>());
        this.bodies.put(name, new Hashtable<>());
    }

    public DbEntityBuilder setProject(String key, Project project) {
        this.projects.put(key, project);
        return this;
    }

    public DbEntityBuilder setVersion(ProjectVersion projectVersion) {
        Project project = projectVersion.getProject();
        String projectName = project.getName();
        if (!this.projects.containsKey(projectName)) {
            setProject(projectName, project);
        }
        addEntry(this.versions, projectVersion.getProject().getName(), projectVersion);
        return this;
    }

    public boolean hasDocument(String projectName,
                               String documentName) {
        assertProjectExists(this.documents, projectName);
        return this.documents.get(projectName).containsKey(documentName);
    }

    public DbEntityBuilder newDocument(String projectName,
                                       String docName,
                                       String docDescription) {
        Project project = this.getProject(projectName);
        Document document = new Document(null, project, docName, docDescription);
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
        ProjectVersion projectVersion = versionService.createNewVersion(project,
            MAJOR_VERSION,
            MINOR_VERSION,
            this.revisionNumber++);
        addEntry(this.versions, projectName, projectVersion);
        return this;
    }

    public ArtifactType newTypeAndReturn(String projectName, String typeName) {
        return this.newType(projectName, typeName).getType(projectName, typeName);
    }

    public DbEntityBuilder newType(String projectName, String typeName) {
        Project project = getProject(projectName);
        ArtifactType artifactType = this.artifactTypeService.createArtifactType(project, typeName, currentUser);
        addEntry(this.artifactTypes, projectName, typeName, artifactType);
        return this;
    }

    public boolean hasType(String projectName, String typeName) {
        assertProjectExists(this.artifactTypes, projectName);
        return this.artifactTypes.get(projectName).containsKey(typeName);
    }

    public DbEntityBuilder newCustomAttribute(String projectName, CustomAttributeType type, String label, String key) {
        newCustomAttributeWithReturn(projectName, type, label, key);
        return this;
    }

    public CustomAttribute newCustomAttributeWithReturn(String projectName, CustomAttributeType type,
                                                        String label, String key) {
        Project project = getProject(projectName);

        CustomAttribute field = new CustomAttribute();
        field.setProject(project);
        field.setType(type);
        field.setLabel(label);
        field.setKeyname(key);

        field = this.customAttributeRepository.save(field);
        AttributesForTesting.addExtraInfo(field, attributeSystemServiceProvider);
        return field;
    }

    public Artifact newArtifactWithReturn(String projectName, String typeName, String artifactName) {
        return this.newArtifact(projectName, typeName, artifactName).getArtifact(projectName, artifactName);
    }

    public DbEntityBuilder newArtifact(String projectName,
                                       String typeName,
                                       String artifactName) {
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
        this.newTraceLinkWithReturn(projectName, sourceName, targetName, projectVersionIndex);
        return this;
    }

    public TraceLinkVersion newTraceLinkWithReturn(String projectName,
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
            .withModificationType(ModificationType.ADDED)
            .withManualTraceType();
        traceLinkVersion.setApprovalStatus(ApprovalStatus.APPROVED);
        return this.traceLinkVersionRepository.save(traceLinkVersion);
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

    public Organization newOrganization(String name, String description) {
        return organizationService.createNewOrganization(new Organization(name, description, currentUser, PaymentTier.AS_NEEDED, false));
    }

    public Team newTeam(String name, Organization organization) {
        return teamService.createNewTeam(name, organization, false, currentUser);
    }

    private <T> void assertProjectExists(Map<String, T> table, String projectName) {
        assertEntityExists(table, projectName, "Project");
    }

    public IEntityMembership createMembershipWithReturn(IEntityWithMembership membershipEntity, SafaUser user, IRole role) {
        if (role instanceof ProjectRole && membershipEntity instanceof Project) {
            return projectMembershipService.addUserRole(user, membershipEntity, role);
        } else if (role instanceof TeamRole && membershipEntity instanceof Team) {
            return teamMembershipService.addUserRole(user, membershipEntity, role);
        } else if (role instanceof OrganizationRole && membershipEntity instanceof Organization) {
            return organizationMembershipService.addUserRole(user, membershipEntity, role);
        } else {
            throw new AssertionError("Role type does not match membership entity type");
        }
    }

    public DbEntityBuilder createMembership(IEntityWithMembership membershipEntity, SafaUser user, IRole role) {
        createMembershipWithReturn(membershipEntity, user, role);
        return this;
    }

    public void deleteMembership(IEntityWithMembership membershipEntity, SafaUser user, IRole role) {
        if (role instanceof ProjectRole && membershipEntity instanceof Project) {
            projectMembershipService.removeUserRole(user, membershipEntity, role);
        } else if (role instanceof TeamRole && membershipEntity instanceof Team) {
            teamMembershipService.removeUserRole(user, membershipEntity, role);
        } else if (role instanceof OrganizationRole && membershipEntity instanceof Organization) {
            organizationMembershipService.removeUserRole(user, membershipEntity, role);
        } else {
            throw new AssertionError("Role type does not match membership entity type");
        }
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
