package edu.nd.crc.safa.features.permissions.checks.billing;

import edu.nd.crc.safa.features.billing.services.CostEstimationService;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;

public class CanAffordHgenCheck extends CanAffordChargeCheck {

    public CanAffordHgenCheck(HGenRequest hGenRequest) {
        super(context -> getHgenPrice(context, hGenRequest));
    }

    private static int getHgenPrice(PermissionCheckContext context, HGenRequest hGenRequest) {
        CostEstimationService costEstimationService = context.getServiceProvider().getCostEstimationService();
        return costEstimationService.estimateHgen(hGenRequest.getArtifacts().size(),
            hGenRequest.getTargetTypes().size());
    }
}
