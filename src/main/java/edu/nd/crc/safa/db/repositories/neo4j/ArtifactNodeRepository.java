package edu.nd.crc.safa.db.repositories.neo4j;

import edu.nd.crc.safa.db.entities.neo4j.ArtifactNode;

import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactNodeRepository extends Neo4jRepository<ArtifactNode, String> {
}
