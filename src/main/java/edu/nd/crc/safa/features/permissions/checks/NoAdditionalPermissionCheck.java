package edu.nd.crc.safa.features.permissions.checks;

public class NoAdditionalPermissionCheck implements AdditionalPermissionCheck {
    @Override
    public boolean doCheck(PermissionCheckContext context) {
        return true;
    }
}
