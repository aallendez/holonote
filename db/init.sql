-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR PRIMARY KEY,
    user_name VARCHAR NOT NULL,
    user_email VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Create index on email for better query performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Create entries table
CREATE TABLE IF NOT EXISTS entries (
    entry_id VARCHAR PRIMARY KEY,
    user_id VARCHAR FOREIGN KEY REFERENCES users(user_id) NOT NULL,
    entry_date TIMESTAMP NOT NULL,
    title VARCHAR NOT NULL,
    content VARCHAR NOT NULL,
    score INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Create entries_tags table
CREATE TABLE IF NOT EXISTS entries_tags (
    entry_tag_id VARCHAR PRIMARY KEY,
    entry_id VARCHAR FOREIGN KEY REFERENCES entries(entry_id) NOT NULL,
    tag_id VARCHAR FOREIGN KEY REFERENCES tags(tag_id) NOT NULL,
);

CREATE TABLE IF NOT EXISTS tags (
    tag_id VARCHAR PRIMARY KEY,
    tag_name VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Create index on user_id for better query performance
CREATE INDEX IF NOT EXISTS idx_entries_user_id ON entries(user_id);
CREATE INDEX IF NOT EXISTS idx_entries_entry_date ON entries(entry_date);
