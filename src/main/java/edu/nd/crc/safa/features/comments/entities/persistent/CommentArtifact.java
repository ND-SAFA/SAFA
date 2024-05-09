package edu.nd.crc.safa.features.comments.entities.persistent;

import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Getter
@Setter
@Entity
@Table(name = "comment_artifact")
public class CommentArtifact {
    /**
     * ID of record
     */
    @Id
    @JdbcTypeCode(SqlTypes.BINARY)
    @GeneratedValue
    @Column(nullable = false)
    private UUID id;
    /**
     * The comment referencing external artifact.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "comment_id", nullable = false)
    private Comment comment;
    /**
     * The artifact being referenced.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_id", nullable = false)
    private Artifact artifactReferenced;

    /**
     * @return Hash of ID.
     */
    public int hashCode() {
        return this.id.hashCode();
    }

    /**
     * @param obj Object being compared.
     * @return True if IDs match.
     */
    @Override
    public boolean equals(Object obj) {
        if (obj instanceof CommentArtifact commentArtifact) {
            return this.id.equals(commentArtifact.id);
        }
        return false;
    }
}
