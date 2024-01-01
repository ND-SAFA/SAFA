package edu.nd.crc.safa.features.permissions.checks.billing;

import edu.nd.crc.safa.features.billing.services.CostEstimationService;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class CanAffordHgenCheck implements AdditionalPermissionCheck {

    private final HGenRequest hGenRequest;

    public CanAffordHgenCheck(HGenRequest hGenRequest) {
        this.hGenRequest = hGenRequest;
    }

    @Override
    public boolean doCheck(PermissionCheckContext context) {
        ProjectVersion version = context.getProjectVersion();
        assert version != null : "Context did not contain a project version";

        CostEstimationService costEstimationService = context.getServiceProvider().getCostEstimationService();
        int price = costEstimationService.estimateHgen(version, hGenRequest.getTargetTypes().size());

        return new CanAffordChargeCheck(price).doCheck(context);
    }
}
