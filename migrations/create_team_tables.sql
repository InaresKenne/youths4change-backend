-- Team Members and Founder Tables for Youths4Change

-- Table for founder information
CREATE TABLE IF NOT EXISTS founder (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    bio TEXT NOT NULL,
    image_url TEXT,
    image_public_id VARCHAR(255),
    email VARCHAR(255),
    linkedin_url TEXT,
    twitter_url TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for team members
CREATE TABLE IF NOT EXISTS team_members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    role_type VARCHAR(50) NOT NULL, -- 'executive', 'board', 'volunteer', 'advisor'
    bio TEXT,
    image_url TEXT,
    image_public_id VARCHAR(255),
    email VARCHAR(255),
    linkedin_url TEXT,
    twitter_url TEXT,
    country VARCHAR(100),
    order_position INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default founder data (you can update this later from admin panel)
INSERT INTO founder (name, title, bio, is_active) 
VALUES (
    'Founder Name',
    'Founder & Executive Director',
    'Write the founder''s biography here. This can include their vision, background, and what inspired them to start Youths4Change Initiative.',
    true
) ON CONFLICT DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_team_members_role_type ON team_members(role_type);
CREATE INDEX IF NOT EXISTS idx_team_members_active ON team_members(is_active);
CREATE INDEX IF NOT EXISTS idx_team_members_order ON team_members(order_position);

-- Add sample team members (optional - remove if not needed)
INSERT INTO team_members (name, position, role_type, bio, country, order_position, is_active)
VALUES 
    ('Team Member 1', 'Vice President', 'executive', 'Brief bio about this team member and their role.', 'Kenya', 1, true),
    ('Team Member 2', 'Program Director', 'executive', 'Brief bio about this team member and their role.', 'Uganda', 2, true),
    ('Team Member 3', 'Board Member', 'board', 'Brief bio about this board member.', 'Tanzania', 3, true)
ON CONFLICT DO NOTHING;
