const express = require('express');
const { PrismaClient } = require('@prisma/client');
const auth = require('../middleware/auth');

const router = express.Router();
const prisma = new PrismaClient();

router.use(auth);

// Get all cookies for a profile
router.get('/profile/:profileId', async (req, res) => {
  try {
    const cookies = await prisma.cookie.findMany({
      where: {
        profileId: parseInt(req.params.profileId),
      },
    });
    res.json(cookies);
  } catch (error) {
    res.status(400).json({ error: 'Failed to get cookies' });
  }
});

// Add cookie to profile
router.post('/profile/:profileId', async (req, res) => {
  try {
    const { domain, name, value, path } = req.body;
    const cookie = await prisma.cookie.create({
      data: {
        domain,
        name,
        value,
        path,
        profileId: parseInt(req.params.profileId),
      },
    });
    res.json(cookie);
  } catch (error) {
    res.status(400).json({ error: 'Failed to create cookie' });
  }
});

// Delete cookie
router.delete('/:id', async (req, res) => {
  try {
    await prisma.cookie.delete({
      where: {
        id: parseInt(req.params.id),
      },
    });
    res.json({ message: 'Cookie deleted' });
  } catch (error) {
    res.status(400).json({ error: 'Failed to delete cookie' });
  }
});

module.exports = router;