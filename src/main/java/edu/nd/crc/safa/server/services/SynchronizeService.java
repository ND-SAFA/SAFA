package edu.nd.crc.safa.server.services;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import edu.nd.crc.safa.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.entities.sql.TraceLink;
import edu.nd.crc.safa.db.repositories.sql.ArtifactBodyRepository;
import edu.nd.crc.safa.db.repositories.sql.TraceLinkRepository;
import edu.nd.crc.safa.server.responses.ServerError;

import com.jsoniter.output.JsonStream;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class SynchronizeService {

    Neo4JService neo4JService;
    ArtifactBodyRepository artifactBodyRepository;
    TraceLinkRepository traceLinkRepository;

    Set<String> foundNodes;

    @Autowired
    public SynchronizeService(ArtifactBodyRepository artifactBodyRepository,
                              TraceLinkRepository traceLinkRepository,
                              Neo4JService neo4JService) {
        this.artifactBodyRepository = artifactBodyRepository;
        this.traceLinkRepository = traceLinkRepository;
        this.neo4JService = neo4JService;
        this.foundNodes = new HashSet<>();
    }

    public void projectPull(ProjectVersion projectVersion) throws ServerError {
        Project project = projectVersion.getProject();
        this.mySQLNeo(project, projectVersion);
        this.neo4JService.execute();
    }

    public void mySQLNeo(Project project, ProjectVersion projectVersion) throws ServerError {
        insertArtifacts(projectVersion);
        insertConnections(project);
    }

    public void insertArtifacts(ProjectVersion projectVersion) {
        List<ArtifactBody> artifacts = this.artifactBodyRepository.findByProjectVersion(projectVersion);
        for (ArtifactBody artifact : artifacts) {
            String type = artifact.getTypeName();
            String id = artifact.getName();
            String summary = artifact.getSummary();
            String content = artifact.getContent();

            Map<String, Object> data = new HashMap<String, Object>();
            data.put("source", "Flatfile");
            data.put("isDelegated", "N/A");
            data.put("status", "N/A");
            data.put("name", summary);
            data.put("href", "N/A");
            data.put("description", content);
            data.put("type", type);

            this.foundNodes.add(id);
            this.neo4JService.addNode(id, type, JsonStream.serialize(data));
        }
    }

    public void insertConnections(Project project) {
        List<TraceLink> projectLinks = traceLinkRepository.findByProject(project);
        for (TraceLink link : projectLinks) {
            if (link.isApproved()) {
                this.neo4JService.addLink(link.getSourceName(),
                    link.getTraceType().toString(),
                    link.getTargetName());
            }
        }
    }
}
