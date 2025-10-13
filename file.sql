
CREATE TABLE profile_seekers (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) UNIQUE,
  full_name VARCHAR(100) NOT NULL,
  tagline VARCHAR(200),
  bio TEXT,
  skills TEXT,
  location VARCHAR(100),
  profile_picture_url VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE applications (
  id SERIAL PRIMARY KEY,
  job_id INTEGER REFERENCES jobs(id),
  seeker_id INTEGER REFERENCES users(id),
  proposal_message TEXT NOT NULL,
  proposed_rate DECIMAL(10,2),
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW()
);
