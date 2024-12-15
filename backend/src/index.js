import express from 'express';
import configureServer from './config/server.js';
import authRoutes from './routes/auth.js';
import cookieRoutes from './routes/cookies.js';
import proxyRoutes from './routes/proxies.js';

const app = express();
configureServer(app);

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/cookies', cookieRoutes);
app.use('/api/proxies', proxyRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});