package edu.nd.crc.safa.features.billing.controllers;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.features.billing.services.IBillingService;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class TempStripeController extends BaseController {

    private final IBillingService billingService;

    public TempStripeController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                IBillingService billingService) {
        super(resourceBuilder, serviceProvider);
        this.billingService = billingService;
    }

    @GetMapping("/stripe/checkout")
    public String getCheckoutUrl() {
        return billingService.startTransaction("foo");
    }
}
