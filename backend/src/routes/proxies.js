import express from 'express';
import { getProxies, createProxy, deleteProxy } from '../controllers/proxyController.js';
import { auth } from '../middleware/auth.js';

const router = express.Router();

router.use(auth);

router.get('/', getProxies);
router.post('/', createProxy);
router.delete('/:id', deleteProxy);

export default router;