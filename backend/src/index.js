const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { PrismaClient } = require('@prisma/client');
const authRoutes = require('./routes/auth');
const cookieRoutes = require('./routes/cookies');
const proxyRoutes = require('./routes/proxies');

const prisma = new PrismaClient();
const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/cookies', cookieRoutes);
app.use('/api/proxies', proxyRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});