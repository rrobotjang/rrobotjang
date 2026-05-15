package com.rrobotjang.userprofileservice.profile;

import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
public class UserProfileService {
    private final UserProfileRepository repository;

    public UserProfileService(UserProfileRepository repository) {
        this.repository = repository;
    }

    @Cacheable(cacheNames = "profiles", key = "#userId")
    public UserProfile getProfile(String userId) {
        return repository.findById(userId)
            .orElseThrow(() -> new IllegalArgumentException("Profile not found: " + userId));
    }

    @CacheEvict(cacheNames = "profiles", key = "#request.userId")
    public UserProfile upsert(UpsertProfileRequest request) {
        UserProfile profile = repository.findById(request.userId())
            .map(existing -> {
                existing.setEmail(request.email());
                existing.setDisplayName(request.displayName());
                return existing;
            })
            .orElseGet(() -> new UserProfile(request.userId(), request.email(), request.displayName()));
        return repository.save(profile);
    }

    public record UpsertProfileRequest(String userId, String email, String displayName) {}
}
