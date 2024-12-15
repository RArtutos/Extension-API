import { PrismaClient } from '@prisma/client';
import { hashPassword } from '../src/utils/auth.js';

const prisma = new PrismaClient();

async function main() {
  try {
    // Crear usuario por defecto
    const hashedPassword = await hashPassword('artutos123');
    
    await prisma.user.upsert({
      where: { email: 'admin@artutos.eu.org' },
      update: {},
      create: {
        email: 'admin@artutos.eu.org',
        password: hashedPassword,
      },
    });

    console.log('Base de datos sembrada exitosamente');
  } catch (error) {
    console.error('Error al sembrar la base de datos:', error);
    throw error;
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });