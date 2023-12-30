package edu.nd.crc.safa.features.permissions.checks;

/**
 * This is a convenience class used to give names to checks which
 * are made up of smaller checks
 */
public abstract class CompositeCheck implements AdditionalPermissionCheck {

    private final AdditionalPermissionCheck subcheck;

    public CompositeCheck(AdditionalPermissionCheck subcheck) {
        this.subcheck = subcheck;
    }

    @Override
    public boolean doCheck(PermissionCheckContext context) {
        return subcheck.doCheck(context);
    }
}
