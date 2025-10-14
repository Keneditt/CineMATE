// routes/applications.js
router.post('/', auth, async (req, res) => {
  try {
    const { job_id, proposal_message, proposed_rate } = req.body;
    const application = await Application.create({
      job_id,
      seeker_id: req.user.id,
      proposal_message,
      proposed_rate
    });
    res.json(application);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// routes/profile.js  
router.post('/seeker', auth, async (req, res) => {
  try {
    const profileData = { ...req.body, user_id: req.user.id };
    // Upsert logic - update if exists, else create
    const profile = await ProfileSeeker.upsert(profileData);
    res.json(profile);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
