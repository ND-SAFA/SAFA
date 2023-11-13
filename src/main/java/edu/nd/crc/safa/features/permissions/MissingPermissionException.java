package edu.nd.crc.safa.features.permissions;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;

@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage", "exception", "errors"})
@Getter
public class MissingPermissionException extends SafaError {

    @JsonIgnore
    private final Set<Permission> missingPermissions;

    public MissingPermissionException(Set<Permission> missingPermissions, boolean needAll) {
        super("Missing permissions. User must have " + (needAll ? "all" : "any") + " of these permissions: "
            + missingPermissions);
        this.missingPermissions = missingPermissions;
    }

    public MissingPermissionException(Permission missingPermission) {
        this(Set.of(missingPermission), true);
    }

    public List<String> getPermissions() {
        return missingPermissions.stream().map(Permission::getName).collect(Collectors.toUnmodifiableList());
    }
}
