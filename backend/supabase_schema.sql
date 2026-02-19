-- DateKeeper Database Schema for Supabase PostgreSQL
-- Run this in Supabase SQL Editor to create all tables

-- ============================================
-- USERS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    phone VARCHAR(20),
    
    -- Notification preferences
    notify_email VARCHAR(1) DEFAULT 'Y',
    notify_sms VARCHAR(1) DEFAULT 'N',
    alternate_email VARCHAR(255),
    
    -- Reminder preferences (JSON)
    reminder_intervals TEXT,
    
    -- Subscription fields
    subscription_tier VARCHAR(20) DEFAULT 'free',
    subscription_status VARCHAR(20) DEFAULT 'active',
    razorpay_subscription_id VARCHAR(255),
    document_limit VARCHAR(10) DEFAULT '10',
    
    -- Account status
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ============================================
-- DOCUMENTS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    document_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    expiry_date DATE NOT NULL,
    reminder_sent JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(20) DEFAULT 'valid',
    
    -- Notification preferences (copied from user at creation)
    email VARCHAR(255),
    phone VARCHAR(20),
    notify_email VARCHAR(1) DEFAULT 'Y',
    notify_sms VARCHAR(1) DEFAULT 'N',
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);
CREATE INDEX IF NOT EXISTS idx_documents_expiry_date ON documents(expiry_date);
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);

-- ============================================
-- FOREIGN KEY CONSTRAINTS
-- ============================================

-- Add foreign key constraint (optional, but recommended)
-- ALTER TABLE documents 
-- ADD CONSTRAINT fk_documents_user_id 
-- FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- ============================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for users table
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for documents table
DROP TRIGGER IF EXISTS update_documents_updated_at ON documents;
CREATE TRIGGER update_documents_updated_at
    BEFORE UPDATE ON documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- ROW LEVEL SECURITY (RLS) - Optional but Recommended
-- ============================================

-- Enable RLS on tables
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- RLS Policies (uncomment if using Supabase Auth)
-- CREATE POLICY "Users can view own profile"
-- ON users FOR SELECT
-- USING (auth.uid()::text = id);

-- CREATE POLICY "Users can update own profile"
-- ON users FOR UPDATE
-- USING (auth.uid()::text = id);

-- CREATE POLICY "Users can view own documents"
-- ON documents FOR SELECT
-- USING (auth.uid()::text = user_id);

-- CREATE POLICY "Users can insert own documents"
-- ON documents FOR INSERT
-- WITH CHECK (auth.uid()::text = user_id);

-- CREATE POLICY "Users can update own documents"
-- ON documents FOR UPDATE
-- USING (auth.uid()::text = user_id);

-- CREATE POLICY "Users can delete own documents"
-- ON documents FOR DELETE
-- USING (auth.uid()::text = user_id);

-- ============================================
-- SAMPLE DATA (Optional - for testing)
-- ============================================

-- Uncomment to insert sample data
-- INSERT INTO users (id, email, hashed_password, full_name, phone, subscription_tier)
-- VALUES 
--     ('test-user-1', 'test@example.com', '$2b$12$...', 'Test User', '+1234567890', 'free');

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check tables were created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE';

-- Check indexes
SELECT indexname, tablename 
FROM pg_indexes 
WHERE schemaname = 'public';

-- Check triggers
SELECT trigger_name, event_object_table 
FROM information_schema.triggers 
WHERE trigger_schema = 'public';

-- ============================================
-- USEFUL QUERIES FOR MONITORING
-- ============================================

-- Count users by subscription tier
-- SELECT subscription_tier, COUNT(*) 
-- FROM users 
-- GROUP BY subscription_tier;

-- Count documents by status
-- SELECT status, COUNT(*) 
-- FROM documents 
-- GROUP BY status;

-- Find expiring documents (next 30 days)
-- SELECT d.*, u.email 
-- FROM documents d
-- JOIN users u ON d.user_id = u.id
-- WHERE d.expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'
-- ORDER BY d.expiry_date;
