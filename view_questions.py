#!/usr/bin/env python3
"""
Script para consultar e visualizar dados do banco de questões do ENEM.
"""

import sqlite3
import json
from typing import List, Dict, Optional


class EnemQuestionViewer:
    def __init__(self, db_path: str = "enem_questions.db"):
        """
        Inicializa o visualizador de questões do ENEM.
        
        Args:
            db_path: Caminho para o arquivo do banco de dados SQLite
        """
        self.db_path = db_path
    
    def get_question_by_id(self, question_id: int) -> Optional[Dict]:
        """Busca uma questão pelo ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                q.id, q.title, q.index_number, q.year, q.context,
                q.alternatives_introduction, q.correct_alternative,
                d.label as discipline_label, d.value as discipline_value,
                l.label as language_label, l.value as language_value
            FROM questions q
            LEFT JOIN disciplines d ON q.discipline_id = d.id
            LEFT JOIN languages l ON q.language_id = l.id
            WHERE q.id = ?
        ''', (question_id,))
        
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return None
        
        question = {
            'id': result[0],
            'title': result[1],
            'index': result[2],
            'year': result[3],
            'context': result[4],
            'alternatives_introduction': result[5],
            'correct_alternative': result[6],
            'discipline': {
                'label': result[7],
                'value': result[8]
            },
            'language': {
                'label': result[9],
                'value': result[10]
            } if result[9] else None
        }
        
        # Buscar alternativas
        cursor.execute('''
            SELECT letter, text, file_path, is_correct
            FROM alternatives
            WHERE question_id = ?
            ORDER BY letter
        ''', (question_id,))
        
        alternatives = []
        for alt in cursor.fetchall():
            alternatives.append({
                'letter': alt[0],
                'text': alt[1],
                'file': alt[2],
                'is_correct': bool(alt[3])
            })
        
        question['alternatives'] = alternatives
        
        # Buscar arquivos
        cursor.execute('''
            SELECT file_path
            FROM question_files
            WHERE question_id = ?
        ''', (question_id,))
        
        files = [row[0] for row in cursor.fetchall()]
        question['files'] = files
        
        conn.close()
        return question
    
    def search_questions(self, year: Optional[int] = None, 
                        discipline: Optional[str] = None,
                        language: Optional[str] = None,
                        limit: int = 10) -> List[Dict]:
        """
        Busca questões com filtros.
        
        Args:
            year: Ano do exame
            discipline: Valor da disciplina
            language: Valor do idioma
            limit: Limite de resultados
            
        Returns:
            Lista de questões
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                q.id, q.title, q.index_number, q.year,
                d.label as discipline_label, d.value as discipline_value,
                l.label as language_label, l.value as language_value
            FROM questions q
            LEFT JOIN disciplines d ON q.discipline_id = d.id
            LEFT JOIN languages l ON q.language_id = l.id
            WHERE 1=1
        '''
        
        params = []
        
        if year:
            query += ' AND q.year = ?'
            params.append(year)
        
        if discipline:
            query += ' AND d.value = ?'
            params.append(discipline)
        
        if language:
            query += ' AND l.value = ?'
            params.append(language)
        
        query += ' ORDER BY q.year DESC, q.index_number ASC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        
        questions = []
        for row in cursor.fetchall():
            questions.append({
                'id': row[0],
                'title': row[1],
                'index': row[2],
                'year': row[3],
                'discipline': {
                    'label': row[4],
                    'value': row[5]
                },
                'language': {
                    'label': row[6],
                    'value': row[7]
                } if row[6] else None
            })
        
        conn.close()
        return questions
    
    def get_random_question(self, year: Optional[int] = None,
                           discipline: Optional[str] = None) -> Optional[Dict]:
        """Retorna uma questão aleatória."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT q.id
            FROM questions q
            LEFT JOIN disciplines d ON q.discipline_id = d.id
            WHERE 1=1
        '''
        
        params = []
        
        if year:
            query += ' AND q.year = ?'
            params.append(year)
        
        if discipline:
            query += ' AND d.value = ?'
            params.append(discipline)
        
        query += ' ORDER BY RANDOM() LIMIT 1'
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return self.get_question_by_id(result[0])
        return None
    
    def export_questions_to_json(self, filename: str = "enem_questions_export.json",
                                year: Optional[int] = None,
                                discipline: Optional[str] = None):
        """Exporta questões para um arquivo JSON."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                q.id, q.title, q.index_number, q.year, q.context,
                q.alternatives_introduction, q.correct_alternative,
                d.label as discipline_label, d.value as discipline_value,
                l.label as language_label, l.value as language_value
            FROM questions q
            LEFT JOIN disciplines d ON q.discipline_id = d.id
            LEFT JOIN languages l ON q.language_id = l.id
            WHERE 1=1
        '''
        
        params = []
        
        if year:
            query += ' AND q.year = ?'
            params.append(year)
        
        if discipline:
            query += ' AND d.value = ?'
            params.append(discipline)
        
        query += ' ORDER BY q.year DESC, q.index_number ASC'
        
        cursor.execute(query, params)
        
        questions = []
        for row in cursor.fetchall():
            question_id = row[0]
            
            # Buscar alternativas
            cursor.execute('''
                SELECT letter, text, file_path, is_correct
                FROM alternatives
                WHERE question_id = ?
                ORDER BY letter
            ''', (question_id,))
            
            alternatives = []
            for alt in cursor.fetchall():
                alternatives.append({
                    'letter': alt[0],
                    'text': alt[1],
                    'file': alt[2],
                    'is_correct': bool(alt[3])
                })
            
            # Buscar arquivos
            cursor.execute('''
                SELECT file_path
                FROM question_files
                WHERE question_id = ?
            ''', (question_id,))
            
            files = [f[0] for f in cursor.fetchall()]
            
            question = {
                'id': row[0],
                'title': row[1],
                'index': row[2],
                'year': row[3],
                'context': row[4],
                'alternatives_introduction': row[5],
                'correct_alternative': row[6],
                'discipline': {
                    'label': row[7],
                    'value': row[8]
                },
                'language': {
                    'label': row[9],
                    'value': row[10]
                } if row[9] else None,
                'alternatives': alternatives,
                'files': files
            }
            
            questions.append(question)
        
        conn.close()
        
        # Salvar em arquivo JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Exportadas {len(questions)} questões para {filename}")
    
    def print_question(self, question: Dict):
        """Imprime uma questão formatada."""
        print(f"\n{'='*60}")
        print(f"📝 {question['title']}")
        print(f"📅 Ano: {question['year']} | 📊 Questão: {question['index']}")
        print(f"📚 Disciplina: {question['discipline']['label']}")
        
        if question['language']:
            print(f"🌐 Idioma: {question['language']['label']}")
        
        if question['context']:
            print(f"\n📖 Contexto:")
            print(question['context'])
        
        if question['alternatives_introduction']:
            print(f"\n❓ {question['alternatives_introduction']}")
        
        print(f"\n📋 Alternativas:")
        for alt in question['alternatives']:
            marker = "✅" if alt['is_correct'] else "  "
            print(f"{marker} {alt['letter']}) {alt['text']}")
        
        print(f"\n🎯 Resposta correta: {question['correct_alternative']}")
        
        if question['files']:
            print(f"\n📎 Arquivos: {', '.join(question['files'])}")
        
        print(f"{'='*60}")


def main():
    """Função principal para demonstrar o uso do visualizador."""
    viewer = EnemQuestionViewer()
    
    print("🔍 VISUALIZADOR DE QUESTÕES DO ENEM")
    print("=" * 50)
    
    # Exemplos de uso
    print("\n1. Buscando questões de 2023:")
    questions_2023 = viewer.search_questions(year=2023, limit=3)
    for q in questions_2023:
        print(f"  - {q['title']} ({q['discipline']['label']})")
    
    print("\n2. Buscando questões de matemática:")
    math_questions = viewer.search_questions(discipline="matematica", limit=3)
    for q in math_questions:
        print(f"  - {q['title']} ({q['year']})")
    
    print("\n3. Questão aleatória:")
    random_question = viewer.get_random_question()
    if random_question:
        viewer.print_question(random_question)
    
    print("\n4. Exportando questões de 2023 para JSON:")
    viewer.export_questions_to_json("enem_2023.json", year=2023)


if __name__ == "__main__":
    main()
