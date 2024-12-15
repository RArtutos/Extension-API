import { PrismaClient } from '@prisma/client';
import { hashPassword } from '../src/utils/auth.js';

const prisma = new PrismaClient();

async function main() {
  try {
    // Create admin user
    const hashedPassword = await hashPassword('admin');
    
    await prisma.user.upsert({
      where: { email: 'admin' },
      update: {},
      create: {
        email: 'admin',
        password: hashedPassword,
      },
    });

    console.log('Database seeded successfully');
  } catch (error) {
    console.error('Seeding error:', error);
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