const express = require('express');
const { PrismaClient } = require('@prisma/client');
const auth = require('../middleware/auth');

const router = express.Router();
const prisma = new PrismaClient();

router.use(auth);

// Get all proxies
router.get('/', async (req, res) => {
  try {
    const proxies = await prisma.proxy.findMany({
      where: {
        profiles: {
          some: {
            userId: req.user.id,
          },
        },
      },
    });
    res.json(proxies);
  } catch (error) {
    res.status(400).json({ error: 'Failed to get proxies' });
  }
});

// Create proxy
router.post('/', async (req, res) => {
  try {
    const { host, port, username, password } = req.body;
    const proxy = await prisma.proxy.create({
      data: {
        host,
        port,
        username,
        password,
      },
    });
    res.json(proxy);
  } catch (error) {
    res.status(400).json({ error: 'Failed to create proxy' });
  }
});

// Delete proxy
router.delete('/:id', async (req, res) => {
  try {
    await prisma.proxy.delete({
      where: {
        id: parseInt(req.params.id),
      },
    });
    res.json({ message: 'Proxy deleted' });
  } catch (error) {
    res.status(400).json({ error: 'Failed to delete proxy' });
  }
});

module.exports = router;