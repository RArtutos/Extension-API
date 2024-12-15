import express from 'express';
import { getCookies, createCookie, deleteCookie } from '../controllers/cookieController.js';
import { auth } from '../middleware/auth.js';

const router = express.Router();

router.use(auth);

router.get('/profile/:profileId', getCookies);
router.post('/profile/:profileId', createCookie);
router.delete('/:id', deleteCookie);

export default router;