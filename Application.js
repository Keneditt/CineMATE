// models/Application.js
const applicationSchema = {
  id: { type: 'serial', primaryKey: true },
  job_id: { type: 'integer', foreignKey: 'jobs.id' },
  seeker_id: { type: 'integer', foreignKey: 'users.id' },
  proposal_message: { type: 'text', required: true },
  proposed_rate: { type: 'decimal' }, // optional - if they want to bid differently
  status: { type: 'varchar', default: 'pending' }, // pending, accepted, rejected
  created_at: { type: 'timestamp', default: 'now()' }
};
