package edu.nd.crc.safa.features.permissions;

import java.util.List;
import java.util.Set;

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
        super(getPermissionMessage(missingPermissions, needAll));
        this.missingPermissions = missingPermissions;
    }

    public MissingPermissionException(Permission missingPermission) {
        this(Set.of(missingPermission), true);
    }

    public List<String> getPermissions() {
        return getPermissionNames(missingPermissions);
    }

    private static List<String> getPermissionNames(Set<Permission> permissions) {
        return permissions.stream().map(Permission::getName).toList();
    }

    private static String getPermissionMessage(Set<Permission> missingPermissions, boolean needAll) {
        return
            String.format(
                "Missing permissions. User must have %s of these permissions: %s",
                (needAll ? "all" : "any"),
                getPermissionNames(missingPermissions)
            );
    }
}
