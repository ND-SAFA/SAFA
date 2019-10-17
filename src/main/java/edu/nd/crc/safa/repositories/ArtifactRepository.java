package edu.nd.crc.safa.repositories;

import java.util.Collection;

import org.springframework.data.neo4j.annotation.Query;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

import edu.nd.crc.safa.domain.Artifact;


@RepositoryRestResource(collectionResourceRel = "artifacts", path = "artifacts")
public interface ArtifactRepository extends Neo4jRepository<Artifact, Long> {
  
  Artifact findByName(@Param("name") String name);

  @Query("MATCH (n:Artifact {root: {root}})<-[r:CONSTRAINT_OF]-(m:Artifact) RETURN n,r,m LIMIT {limit}")
	Collection<Artifact> tree(@Param("root") String root, @Param("limit") int limit);
}