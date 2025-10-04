-- USERS
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR PRIMARY KEY,
    user_name VARCHAR NOT NULL,
    user_email VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(user_email);

-- ENTRIES
CREATE TABLE IF NOT EXISTS entries (
    entry_id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(user_id),
    entry_date TIMESTAMP NOT NULL,
    title VARCHAR NOT NULL,
    content VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- HOLO (per-user config; one holo per user)
CREATE TABLE IF NOT EXISTS holo (
    holo_id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    questions JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    UNIQUE (user_id)  -- each user can only have one holo config
);

-- HOLO_DAILIES (daily answers + score)
CREATE TABLE IF NOT EXISTS holo_dailies (
    holo_daily_id VARCHAR PRIMARY KEY,
    holo_id VARCHAR NOT NULL REFERENCES holo(holo_id) ON DELETE CASCADE,
    entry_date DATE NOT NULL,
    score INTEGER NOT NULL,
    answers JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    UNIQUE (holo_id, entry_date) -- one daily per holo per day
);

-- Useful indexes
CREATE INDEX IF NOT EXISTS idx_entries_user_id ON entries(user_id);
CREATE INDEX IF NOT EXISTS idx_entries_entry_date ON entries(entry_date);

CREATE INDEX IF NOT EXISTS idx_holo_user_id ON holo(user_id);
CREATE INDEX IF NOT EXISTS idx_holo_dailies_holo_id ON holo_dailies(holo_id);
CREATE INDEX IF NOT EXISTS idx_holo_dailies_entry_date ON holo_dailies(entry_date);