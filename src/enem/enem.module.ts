import { Module } from '@nestjs/common';
import { EnemController } from './enem.controller';
import { EnemService } from './enem.service';

@Module({
  controllers: [EnemController],
  providers: [EnemService],
  exports: [EnemService],
})
export class EnemModule {}
