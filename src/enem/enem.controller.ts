import { 
  Controller, 
  Get, 
  Param, 
  Query, 
  ParseIntPipe, 
  NotFoundException 
} from '@nestjs/common';
import { EnemService } from './enem.service';
import { FilterDto } from './dto/filter.dto';
import { QuestionDto } from './dto/question.dto';

@Controller('enem')
export class EnemController {
  constructor(private readonly enemService: EnemService) {}

  @Get('questions')
  async getAllQuestions(@Query() filter: FilterDto) {
    return this.enemService.getAllQuestions(filter);
  }

  @Get('questions/random')
  async getRandomQuestion(@Query() filter: FilterDto): Promise<QuestionDto> {
    const question = await this.enemService.getRandomQuestion(filter);
    if (!question) {
      throw new NotFoundException('No questions found with the specified criteria');
    }
    return question;
  }

  @Get('questions/:id')
  async getQuestionById(@Param('id', ParseIntPipe) id: number): Promise<QuestionDto> {
    const question = await this.enemService.getQuestionById(id);
    if (!question) {
      throw new NotFoundException(`Question with ID ${id} not found`);
    }
    return question;
  }

  @Get('years')
  async getAvailableYears(): Promise<number[]> {
    return this.enemService.getAvailableYears();
  }

  @Get('disciplines')
  async getAvailableDisciplines(): Promise<{ label: string; value: string }[]> {
    return this.enemService.getAvailableDisciplines();
  }

  @Get('languages')
  async getAvailableLanguages(): Promise<{ label: string; value: string }[]> {
    return this.enemService.getAvailableLanguages();
  }
}
