package edu.nd.crc.safa.features.chat.entities.persistent;

import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcType;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;
import org.hibernate.type.descriptor.jdbc.VarcharJdbcType;

@Entity
@Table(name = "chat_share")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ChatShare {
    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.BINARY)
    @Column
    private UUID id;
    /**
     * The chat being shared.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "chat_id",
        nullable = false
    )
    private Chat chat;
    /**
     * The user who the chat is shared with.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "user_id",
        nullable = false
    )
    private SafaUser user;
    /**
     * The permission level associated with shared chat.
     */
    @Column
    @Enumerated(EnumType.STRING)
    @JdbcType(VarcharJdbcType.class)
    private ChatPermission permission;
}
