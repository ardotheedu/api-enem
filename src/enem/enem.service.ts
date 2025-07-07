import { Injectable } from '@nestjs/common';
import { Database } from 'sqlite3';
import { QuestionDto } from './dto/question.dto';
import { FilterDto } from './dto/filter.dto';

@Injectable()
export class EnemService {
  private db: Database;

  constructor() {
    this.db = new Database('enem_questions.db');
  }

  async getAllQuestions(filter: FilterDto): Promise<{
    data: QuestionDto[];
    total: number;
    page: number;
    limit: number;
    totalPages: number;
  }> {
    const { year, discipline, language, page = 1, limit = 10 } = filter;
    const offset = (page - 1) * limit;

    let query = `
      SELECT 
        q.id, q.title, q.index_number, q.year, q.context,
        q.alternatives_introduction, q.correct_alternative,
        d.label as discipline_label, d.value as discipline_value,
        l.label as language_label, l.value as language_value
      FROM questions q
      LEFT JOIN disciplines d ON q.discipline_id = d.id
      LEFT JOIN languages l ON q.language_id = l.id
      WHERE 1=1
    `;

    let countQuery = `
      SELECT COUNT(*) as total
      FROM questions q
      LEFT JOIN disciplines d ON q.discipline_id = d.id
      LEFT JOIN languages l ON q.language_id = l.id
      WHERE 1=1
    `;

    const params: any[] = [];

    if (year) {
      query += ' AND q.year = ?';
      countQuery += ' AND q.year = ?';
      params.push(year);
    }

    if (discipline) {
      query += ' AND d.value = ?';
      countQuery += ' AND d.value = ?';
      params.push(discipline);
    }

    if (language) {
      query += ' AND l.value = ?';
      countQuery += ' AND l.value = ?';
      params.push(language);
    }

    query += ' ORDER BY q.year DESC, q.index_number ASC LIMIT ? OFFSET ?';
    
    const [questions, totalResult] = await Promise.all([
      this.runQuery(query, [...params, limit, offset]),
      this.runQuery(countQuery, params)
    ]);

    const total = (totalResult as any)[0].total;
    const totalPages = Math.ceil(total / limit);

    const data = await Promise.all(
      (questions as any[]).map(async (question) => {
        const alternatives = await this.getAlternatives(question.id);
        const files = await this.getQuestionFiles(question.id);
        
        return {
          id: question.id,
          title: question.title,
          index: question.index_number,
          year: question.year,
          context: question.context,
          alternativesIntroduction: question.alternatives_introduction,
          correctAlternative: question.correct_alternative,
          discipline: question.discipline_label ? {
            label: question.discipline_label,
            value: question.discipline_value
          } : null,
          language: question.language_label ? {
            label: question.language_label,
            value: question.language_value
          } : null,
          alternatives,
          files
        };
      })
    );

    return {
      data,
      total,
      page,
      limit,
      totalPages
    };
  }

  async getQuestionById(id: number): Promise<QuestionDto | null> {
    const query = `
      SELECT 
        q.id, q.title, q.index_number, q.year, q.context,
        q.alternatives_introduction, q.correct_alternative,
        d.label as discipline_label, d.value as discipline_value,
        l.label as language_label, l.value as language_value
      FROM questions q
      LEFT JOIN disciplines d ON q.discipline_id = d.id
      LEFT JOIN languages l ON q.language_id = l.id
      WHERE q.id = ?
    `;

    const result = await this.runQuery(query, [id]);
    const questions = result as any[];

    if (!questions || questions.length === 0) {
      return null;
    }

    const question = questions[0];
    const alternatives = await this.getAlternatives(id);
    const files = await this.getQuestionFiles(id);

    return {
      id: question.id,
      title: question.title,
      index: question.index_number,
      year: question.year,
      context: question.context,
      alternativesIntroduction: question.alternatives_introduction,
      correctAlternative: question.correct_alternative,
      discipline: question.discipline_label ? {
        label: question.discipline_label,
        value: question.discipline_value
      } : null,
      language: question.language_label ? {
        label: question.language_label,
        value: question.language_value
      } : null,
      alternatives,
      files
    };
  }

  async getRandomQuestion(filter: FilterDto): Promise<QuestionDto | null> {
    const { year, discipline, language } = filter;

    let query = `
      SELECT q.id
      FROM questions q
      LEFT JOIN disciplines d ON q.discipline_id = d.id
      LEFT JOIN languages l ON q.language_id = l.id
      WHERE 1=1
    `;

    const params: any[] = [];

    if (year) {
      query += ' AND q.year = ?';
      params.push(year);
    }

    if (discipline) {
      query += ' AND d.value = ?';
      params.push(discipline);
    }

    if (language) {
      query += ' AND l.value = ?';
      params.push(language);
    }

    query += ' ORDER BY RANDOM() LIMIT 1';

    const result = await this.runQuery(query, params);
    const questions = result as any[];

    if (!questions || questions.length === 0) {
      return null;
    }

    return this.getQuestionById(questions[0].id);
  }

  async getAvailableYears(): Promise<number[]> {
    const query = 'SELECT DISTINCT year FROM questions ORDER BY year DESC';
    const results = await this.runQuery(query, []);
    return (results as any[]).map(row => row.year);
  }

  async getAvailableDisciplines(): Promise<{ label: string; value: string }[]> {
    const query = 'SELECT DISTINCT label, value FROM disciplines ORDER BY label';
    const results = await this.runQuery(query, []);
    return (results as any[]).map(row => ({
      label: row.label,
      value: row.value
    }));
  }

  async getAvailableLanguages(): Promise<{ label: string; value: string }[]> {
    const query = 'SELECT DISTINCT label, value FROM languages ORDER BY label';
    const results = await this.runQuery(query, []);
    return (results as any[]).map(row => ({
      label: row.label,
      value: row.value
    }));
  }

  private async getAlternatives(questionId: number): Promise<any[]> {
    const query = `
      SELECT letter, text, file_path, is_correct
      FROM alternatives
      WHERE question_id = ?
      ORDER BY letter
    `;

    const alternatives = await this.runQuery(query, [questionId]);
    return (alternatives as any[]).map(alt => ({
      letter: alt.letter,
      text: alt.text,
      filePath: alt.file_path,
      isCorrect: alt.is_correct === 1
    }));
  }

  private async getQuestionFiles(questionId: number): Promise<string[]> {
    const query = `
      SELECT file_path
      FROM question_files
      WHERE question_id = ?
    `;

    const files = await this.runQuery(query, [questionId]);
    return (files as any[]).map(file => file.file_path);
  }

  private runQuery(query: string, params: any[]): Promise<any> {
    return new Promise((resolve, reject) => {
      this.db.all(query, params, (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }
}
