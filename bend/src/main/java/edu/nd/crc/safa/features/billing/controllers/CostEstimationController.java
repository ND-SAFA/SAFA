package edu.nd.crc.safa.features.billing.controllers;

import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.billing.services.BillingService;
import edu.nd.crc.safa.features.billing.services.CostEstimationService;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;

import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CostEstimationController extends BaseController {

    private final CostEstimationService costEstimationService;
    private final BillingService billingService;

    public CostEstimationController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                    CostEstimationService costEstimationService,
                                    BillingService billingService) {
        super(resourceBuilder, serviceProvider);
        this.costEstimationService = costEstimationService;
        this.billingService = billingService;
    }

    /**
     * Estimates the cost of generating hierarchy above artifacts in request.
     *
     * @param versionId The Id of the version to collect artifacts in.
     * @param request   Contains artifacts and clusters within them.
     * @return List of generates artifacts for new level.
     */
    @PostMapping(AppRoutes.HGen.ESTIMATE)
    public CostEstimationDTO estimateGenerateHierarchy(@PathVariable UUID versionId,
                                                       @RequestBody @Valid HGenRequest request) throws Exception {
        int credits = costEstimationService.estimateHgen(request.getArtifacts().size(),
            request.getTargetTypes().size());
        return createCostEstimation(credits);
    }

    private CostEstimationDTO createCostEstimation(int credits) {
        long pricePerCredit = billingService.getCreditPrice();
        return new CostEstimationDTO(credits, credits * pricePerCredit);
    }

    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    public static class CostEstimationDTO {
        private int credits;
        private long price;
    }
}
