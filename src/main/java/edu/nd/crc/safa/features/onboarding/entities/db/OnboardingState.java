package edu.nd.crc.safa.features.onboarding.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.annotation.Nullable;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "onboarding")
@Getter
@Setter
@ToString
@NoArgsConstructor
public class OnboardingState {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.BINARY)
    @Column
    @NotNull
    private UUID id;

    @NotNull
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column
    private UUID userId;

    @Column
    @NotNull
    private boolean completed;

    @Column
    @Nullable
    @JdbcTypeCode(SqlTypes.VARCHAR)
    private UUID projectId;

    public OnboardingState(SafaUser user) {
        this.userId = user.getUserId();
        this.completed = false;
        this.projectId = null;
    }
}
