package edu.nd.crc.safa.features.permissions;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.permissions.entities.Permission;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;

@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage"})
@Getter
public class MissingPermissionException extends RuntimeException {

    @JsonIgnore
    private final Set<Permission> missingPermissions;

    public MissingPermissionException(Set<Permission> missingPermissions, boolean needAll) {
        super("Missing permissions. User must have " + (needAll ? "all" : "any") + " of these permissions.");
        this.missingPermissions = missingPermissions;
    }

    public MissingPermissionException(Permission missingPermission) {
        super("Missing permission.");
        this.missingPermissions = Set.of(missingPermission);
    }

    public List<String> getPermissions() {
        return missingPermissions.stream().map(Permission::getName).collect(Collectors.toUnmodifiableList());
    }
}
