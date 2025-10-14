// models/ProfileSeeker.js
const profileSeekerSchema = {
  id: { type: 'serial', primaryKey: true },
  user_id: { type: 'integer', foreignKey: 'users.id', unique: true },
  full_name: { type: 'varchar', required: true },
  tagline: { type: 'varchar' }, // 
  bio: { type: 'text' },
  skills: { type: 'text' }, 
  location: { type: 'varchar' },
  profile_picture_url: { type: 'varchar' },
  created_at: { type: 'timestamp', default: 'now()' },
  updated_at: { type: 'timestamp', default: 'now()' }
};
