package edu.nd.crc.safa.features.chat.entities.persistent;

import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.annotation.JsonIgnore;
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
@Table(name = "chat")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Chat {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.BINARY)
    @Column
    private UUID id;
    /**
     * The project version whose artifact's are accessed during chat.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "version_id",
        nullable = false
    )
    @JsonIgnore
    private ProjectVersion projectVersion;
    /**
     * The owner of the chat.
     */
    @ManyToOne
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "owner_id",
        nullable = false
    )
    private SafaUser owner;
    /**
     * Display name of chat.
     */
    @Column
    private String title;

    /**
     * Returns whether user is owner of chat.
     *
     * @param user The user to check.
     * @return True if given user is owner of chat.
     */
    public boolean isOwner(SafaUser user) {
        return this.owner.getUserId().equals(user.getUserId());
    }
}

