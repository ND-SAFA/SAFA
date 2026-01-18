package edu.nd.crc.safa.features.users.entities.db;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Entity for storing encrypted user API keys.
 * Each user can have one set of API keys for OpenAI and Anthropic.
 */
@Entity
@Table(name = "user_api_keys")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserApiKey implements Serializable {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "id")
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false, unique = true)
    private SafaUser user;

    @Column(name = "openai_api_key", length = 512)
    private String openaiApiKey;

    @Column(name = "anthropic_api_key", length = 512)
    private String anthropicApiKey;

    @Column(name = "preferred_provider", length = 50)
    private String preferredProvider = "openai";

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        LocalDateTime now = LocalDateTime.now();
        createdAt = now;
        updatedAt = now;
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
