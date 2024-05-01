package edu.nd.crc.safa.features.comments.entities.persistent;

import java.time.LocalDateTime;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Lob;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.PrePersist;
import jakarta.persistence.PreUpdate;
import jakarta.persistence.Table;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Data
@Entity
@Table(name = "comment")
public class Comment {
    @Id
    @JdbcTypeCode(SqlTypes.BINARY)
    @GeneratedValue
    @Column(nullable = false)
    private UUID id;
    /**
     * The text of the comment.
     */
    @Column(columnDefinition = "mediumtext")
    @Lob
    private String content;
    /**
     * Status of comment (e.g. active | resolved).
     */
    @Column
    @Enumerated(EnumType.STRING)
    @JdbcTypeCode(SqlTypes.VARCHAR)
    private CommentStatus status;
    /**
     * The type of comment
     */
    @Column
    @Enumerated(EnumType.STRING)
    @JdbcTypeCode(SqlTypes.VARCHAR)
    private CommentType type;
    /**
     * Author of comment
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "author_id", nullable = false)
    private SafaUser author;
    /**
     * Artifact being commented on.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_id", nullable = false)
    private Artifact artifact;
    /**
     * Version that comment was created in.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "version_id", nullable = false)
    private ProjectVersion version;
    /**
     * Timestamp of when comment was created.
     */
    @Column
    private LocalDateTime createdAt;
    /**
     * Timestamp of when this comment was last updated.
     */
    @Column
    private LocalDateTime updatedAt;

    /**
     * Whether given user is author of comment.
     *
     * @param user The user to check.
     * @return True if given user is author of comment.
     */
    public boolean isAuthor(SafaUser user) {
        return this.author.getUserId().equals(user.getUserId());
    }

    @PrePersist
    public void setCreatedAt() {
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    public void setUpdatedAt() {
        this.updatedAt = LocalDateTime.now();
    }
}
