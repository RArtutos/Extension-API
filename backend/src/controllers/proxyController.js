import prisma from '../config/database.js';

export const getProxies = async (req, res) => {
  try {
    const proxies = await prisma.proxy.findMany({
      where: {
        profiles: {
          some: {
            userId: req.user.userId,
          },
        },
      },
    });
    res.json(proxies);
  } catch (error) {
    res.status(400).json({ error: 'Failed to get proxies' });
  }
};

export const createProxy = async (req, res) => {
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
};

export const deleteProxy = async (req, res) => {
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
};