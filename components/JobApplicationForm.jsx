// components/JobApplicationForm.jsx
import { useState } from 'react';
import { applyToJob } from '../services/api';

const JobApplicationForm = ({ job, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    proposal_message: '',
    proposed_rate: job.budget_estimate || ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await applyToJob(job.id, formData);
      onSuccess();
      onClose();
    } catch (error) {
      alert('Failed to submit application');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal">
      <h2>Apply to {job.title}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Proposal Message *</label>
          <textarea
            value={formData.proposal_message}
            onChange={(e) => setFormData({...formData, proposal_message: e.target.value})}
            required
            rows={5}
            placeholder="Explain why you're a good fit for this job..."
          />
        </div>
        
        <div>
          <label>Proposed Rate ($)</label>
          <input
            type="number"
            value={formData.proposed_rate}
            onChange={(e) => setFormData({...formData, proposed_rate: e.target.value})}
            placeholder={job.budget_estimate || "Enter your rate"}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Submitting...' : 'Submit Application'}
        </button>
        <button type="button" onClick={onClose}>Cancel</button>
      </form>
    </div>
  );
};
