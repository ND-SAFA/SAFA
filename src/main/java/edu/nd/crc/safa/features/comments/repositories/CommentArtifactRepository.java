package edu.nd.crc.safa.features.comments.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.comments.entities.persistent.CommentArtifact;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CommentArtifactRepository extends CrudRepository<CommentArtifact, UUID> {
    List<CommentArtifact> findAllByComment_IdIn(List<UUID> commentIds);

    List<CommentArtifact> findAllByArtifactReferenced_ArtifactId(UUID artifactId);
}
