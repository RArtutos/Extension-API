import prisma from '../config/database.js';

export const getCookies = async (req, res) => {
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
};

export const createCookie = async (req, res) => {
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
};

export const deleteCookie = async (req, res) => {
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
};