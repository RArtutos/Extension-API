import express from 'express';
import cors from 'cors';
import helmet from 'helmet';

const configureServer = (app) => {
  app.use(helmet());
  app.use(cors());
  app.use(express.json());
};

export default configureServer;