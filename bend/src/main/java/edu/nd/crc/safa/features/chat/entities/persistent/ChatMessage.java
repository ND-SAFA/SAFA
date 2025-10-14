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
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "chat_message")
@Data
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
     * The content of the message.
     */
    @Column(columnDefinition = "mediumtext", nullable = false)
    @Lob
    private String content = "";
    /**
     * Date time of when this message was created.
     */
    @Column(nullable = false, name = "created_at")
    private LocalDateTime createdAt;

    /**
     * Sets the creation time to time instance is created.
     */
    public ChatMessage() {
        this.createdAt = LocalDateTime.now();
    }

    /**
     * Sets content to empty string if null, otherwise content is set to given input.
     *
     * @param content Content to set on comment.
     */
    public void setContent(String content) {
        this.content = content == null ? "" : content;
    }
}
