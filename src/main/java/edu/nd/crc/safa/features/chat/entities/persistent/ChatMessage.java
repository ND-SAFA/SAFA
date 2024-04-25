package edu.nd.crc.safa.features.chat.entities.persistent;

import java.time.LocalDateTime;
import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Lob;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.PrePersist;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "chat_message")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ChatMessage {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.BINARY)
    @Column
    private UUID id;
    /**
     * Whether message originated from user. If false, AI generated.
     */
    @Column(name = "is_user")
    private boolean isUser;
    /**
     * The chat containing message.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "chat_id",
        nullable = false
    )
    @JsonIgnore
    private Chat chat;
    /**
     * The author of the message. Null is AI generated.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "author_id",
        nullable = true
    )
    private SafaUser author;
    /**
     * Date time of when this message was created.
     */
    @Column
    private LocalDateTime created;
    /**
     * The content of the message.
     */
    @Column(columnDefinition = "mediumtext")
    @Lob
    private String content;

    @PrePersist
    public void setCreated() {
        this.created = LocalDateTime.now();
    }
}
