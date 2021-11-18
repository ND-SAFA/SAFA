package edu.nd.crc.safa.server.services;

import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.SafaUserRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class SafaUserService implements UserDetailsService {

    SafaUserRepository safaUserRepository;
    PasswordEncoder passwordEncoder;

    @Autowired
    public SafaUserService(SafaUserRepository safaUserRepository,
                           PasswordEncoder passwordEncoder) {
        this.safaUserRepository = safaUserRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        final SafaUser customer = safaUserRepository.findByEmail(username);
        if (customer == null) {
            throw new UsernameNotFoundException(username);
        }
        return User
            .withUsername(customer.getEmail())
            .password(customer.getPassword())
            .authorities("USER") // TODO: Replace with custom roles here
            .build();
    }

    public SafaUser createNewUser(SafaUser newUser) {
        newUser.setPassword(this.passwordEncoder.encode(newUser.getPassword()));
        this.safaUserRepository.save(newUser);
        return newUser;
    }
}
