package com.rrobotjang.userprofileservice.profile;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "user_profiles")
public class UserProfile {

    @Id
    @Column(nullable = false, length = 100)
    private String userId;

    @Column(nullable = false, length = 100)
    private String email;

    @Column(nullable = false, length = 100)
    private String displayName;

    protected UserProfile() {}

    public UserProfile(String userId, String email, String displayName) {
        this.userId = userId;
        this.email = email;
        this.displayName = displayName;
    }

    public String getUserId() { return userId; }
    public String getEmail() { return email; }
    public String getDisplayName() { return displayName; }

    public void setEmail(String email) { this.email = email; }
    public void setDisplayName(String displayName) { this.displayName = displayName; }
}
