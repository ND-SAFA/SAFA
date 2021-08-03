package edu.nd.crc.safa.services;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.database.entities.Project;
import edu.nd.crc.safa.database.entities.Warning;
import edu.nd.crc.safa.database.repositories.WarningRepository;
import edu.nd.crc.safa.server.error.ServerError;
import edu.nd.crc.safa.warnings.Rule;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class WarningService {

    WarningRepository warningRepository;

    @Autowired
    public WarningService(WarningRepository warningRepository) {
        this.warningRepository = warningRepository;
    }

    public List<Rule> getWarnings(Project project) throws ServerError {
        List<Warning> projectWarnings = this.warningRepository.findAllByProject(project);
        List<Rule> projectRules = new ArrayList<Rule>();

        for (Warning warning : projectWarnings) {
            projectRules.add(new Rule(warning));
        }
        return projectRules;
    }

    public void newWarning(Project project, String nShort, String nLong, String rule) {
        Warning warning = new Warning(project, nShort, nLong, rule);
        this.warningRepository.save(warning);
    }
}
