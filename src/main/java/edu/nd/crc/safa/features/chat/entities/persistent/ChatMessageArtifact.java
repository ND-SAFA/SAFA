package edu.nd.crc.safa.features.chat.entities.persistent;

import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "chat_message_artifact")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ChatMessageArtifact {
    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.BINARY)
    @Column
    private UUID id;
    /**
     * Message referencing artifact.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "message_id",
        nullable = false
    )
    private ChatMessage message;
    /**
     * Artifact referenced in message.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "artifact_id",
        nullable = false
    )
    private Artifact artifact;
}
