#!/usr/bin/env python3
"""
Script para extrair questões do ENEM da pasta quiz-items e armazenar em banco de dados SQLite.
"""

import json
import os
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional


class EnemQuestionExtractor:
    def __init__(self, db_path: str = "enem_questions.db"):
        """
        Inicializa o extrator de questões do ENEM.
        
        Args:
            db_path: Caminho para o arquivo do banco de dados SQLite
        """
        self.db_path = db_path
        self.quiz_items_path = Path("quiz-items")
        
    def create_database(self):
        """Cria as tabelas do banco de dados."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de exames
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de disciplinas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS disciplines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                label TEXT NOT NULL,
                value TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de idiomas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS languages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                label TEXT NOT NULL,
                value TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de questões
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                index_number INTEGER NOT NULL,
                year INTEGER NOT NULL,
                discipline_id INTEGER,
                language_id INTEGER,
                context TEXT,
                alternatives_introduction TEXT,
                correct_alternative TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (discipline_id) REFERENCES disciplines (id),
                FOREIGN KEY (language_id) REFERENCES languages (id),
                UNIQUE(year, index_number, discipline_id, language_id)
            )
        ''')
        
        # Tabela de alternativas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alternatives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                letter TEXT NOT NULL,
                text TEXT NOT NULL,
                file_path TEXT,
                is_correct BOOLEAN NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions (id)
            )
        ''')
        
        # Tabela de arquivos das questões
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS question_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Banco de dados criado com sucesso!")
    
    def insert_disciplines_and_languages(self):
        """Insere disciplinas e idiomas únicos no banco de dados."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Disciplinas padrão do ENEM
        disciplines = [
            ("Ciências Humanas e suas Tecnologias", "ciencias-humanas"),
            ("Ciências da Natureza e suas Tecnologias", "ciencias-natureza"),
            ("Linguagens, Códigos e suas Tecnologias", "linguagens"),
            ("Matemática e suas Tecnologias", "matematica")
        ]
        
        # Idiomas
        languages = [
            ("Espanhol", "espanhol"),
            ("Inglês", "ingles")
        ]
        
        for label, value in disciplines:
            cursor.execute('''
                INSERT OR IGNORE INTO disciplines (label, value) 
                VALUES (?, ?)
            ''', (label, value))
        
        for label, value in languages:
            cursor.execute('''
                INSERT OR IGNORE INTO languages (label, value) 
                VALUES (?, ?)
            ''', (label, value))
        
        conn.commit()
        conn.close()
        print("✅ Disciplinas e idiomas inseridos!")
    
    def get_discipline_id(self, discipline_value: str) -> Optional[int]:
        """Retorna o ID da disciplina pelo valor."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM disciplines WHERE value = ?
        ''', (discipline_value,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def get_language_id(self, language_value: str) -> Optional[int]:
        """Retorna o ID do idioma pelo valor."""
        if not language_value:
            return None
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM languages WHERE value = ?
        ''', (language_value,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def insert_exam(self, title: str, year: int):
        """Insere um exame no banco de dados."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO exams (title, year) 
            VALUES (?, ?)
        ''', (title, year))
        
        conn.commit()
        conn.close()
    
    def insert_question(self, question_data: Dict) -> int:
        """
        Insere uma questão no banco de dados.
        
        Args:
            question_data: Dados da questão
            
        Returns:
            ID da questão inserida
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        discipline_id = self.get_discipline_id(question_data.get('discipline'))
        language_id = self.get_language_id(question_data.get('language'))
        
        cursor.execute('''
            INSERT OR IGNORE INTO questions 
            (title, index_number, year, discipline_id, language_id, context, 
             alternatives_introduction, correct_alternative) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            question_data['title'],
            question_data['index'],
            question_data['year'],
            discipline_id,
            language_id,
            question_data.get('context', ''),
            question_data.get('alternativesIntroduction', ''),
            question_data.get('correctAlternative', '')
        ))
        
        question_id = cursor.lastrowid
        
        # Se a questão já existe, buscar o ID
        if question_id == 0:
            cursor.execute('''
                SELECT id FROM questions 
                WHERE year = ? AND index_number = ? AND discipline_id = ? AND language_id = ?
            ''', (question_data['year'], question_data['index'], discipline_id, language_id))
            result = cursor.fetchone()
            question_id = result[0] if result else None
        
        conn.commit()
        conn.close()
        
        return question_id
    
    def insert_alternatives(self, question_id: int, alternatives: List[Dict]):
        """Insere as alternativas de uma questão."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for alt in alternatives:
            cursor.execute('''
                INSERT OR IGNORE INTO alternatives 
                (question_id, letter, text, file_path, is_correct) 
                VALUES (?, ?, ?, ?, ?)
            ''', (
                question_id,
                alt['letter'],
                alt['text'],
                alt.get('file'),
                alt.get('isCorrect', False)
            ))
        
        conn.commit()
        conn.close()
    
    def insert_question_files(self, question_id: int, files: List[str]):
        """Insere os arquivos de uma questão."""
        if not files:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for file_path in files:
            cursor.execute('''
                INSERT OR IGNORE INTO question_files 
                (question_id, file_path) 
                VALUES (?, ?)
            ''', (question_id, file_path))
        
        conn.commit()
        conn.close()
    
    def extract_questions_from_year(self, year: int):
        """Extrai todas as questões de um ano específico."""
        year_path = self.quiz_items_path / str(year)
        
        if not year_path.exists():
            print(f"⚠️  Pasta do ano {year} não encontrada")
            return
        
        # Ler detalhes do exame
        details_file = year_path / "details.json"
        if not details_file.exists():
            print(f"⚠️  Arquivo details.json não encontrado para {year}")
            return
        
        with open(details_file, 'r', encoding='utf-8') as f:
            exam_details = json.load(f)
        
        # Inserir exame
        self.insert_exam(exam_details['title'], year)
        
        # Processar questões
        questions_path = year_path / "questions"
        if not questions_path.exists():
            print(f"⚠️  Pasta de questões não encontrada para {year}")
            return
        
        questions_processed = 0
        for question_folder in questions_path.iterdir():
            if question_folder.is_dir():
                question_details_file = question_folder / "details.json"
                if question_details_file.exists():
                    try:
                        with open(question_details_file, 'r', encoding='utf-8') as f:
                            question_data = json.load(f)
                        
                        # Inserir questão
                        question_id = self.insert_question(question_data)
                        
                        if question_id:
                            # Inserir alternativas
                            if 'alternatives' in question_data:
                                self.insert_alternatives(question_id, question_data['alternatives'])
                            
                            # Inserir arquivos
                            if 'files' in question_data:
                                self.insert_question_files(question_id, question_data['files'])
                            
                            questions_processed += 1
                    
                    except Exception as e:
                        print(f"❌ Erro ao processar questão {question_folder.name} de {year}: {e}")
        
        print(f"✅ Processadas {questions_processed} questões de {year}")
    
    def extract_all_questions(self):
        """Extrai todas as questões de todos os anos."""
        print("🚀 Iniciando extração de questões do ENEM...")
        
        # Criar banco de dados
        self.create_database()
        
        # Inserir disciplinas e idiomas
        self.insert_disciplines_and_languages()
        
        # Processar cada ano
        for year_folder in self.quiz_items_path.iterdir():
            if year_folder.is_dir() and year_folder.name.isdigit():
                year = int(year_folder.name)
                print(f"📚 Processando ano {year}...")
                self.extract_questions_from_year(year)
        
        print("✅ Extração concluída!")
    
    def get_statistics(self):
        """Exibe estatísticas do banco de dados."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total de questões
        cursor.execute('SELECT COUNT(*) FROM questions')
        total_questions = cursor.fetchone()[0]
        
        # Questões por ano
        cursor.execute('''
            SELECT year, COUNT(*) 
            FROM questions 
            GROUP BY year 
            ORDER BY year
        ''')
        by_year = cursor.fetchall()
        
        # Questões por disciplina
        cursor.execute('''
            SELECT d.label, COUNT(*) 
            FROM questions q 
            JOIN disciplines d ON q.discipline_id = d.id 
            GROUP BY d.label 
            ORDER BY COUNT(*) DESC
        ''')
        by_discipline = cursor.fetchall()
        
        conn.close()
        
        print("\n📊 ESTATÍSTICAS DO BANCO DE DADOS")
        print("=" * 50)
        print(f"Total de questões: {total_questions}")
        
        print("\n📅 Questões por ano:")
        for year, count in by_year:
            print(f"  {year}: {count} questões")
        
        print("\n📖 Questões por disciplina:")
        for discipline, count in by_discipline:
            print(f"  {discipline}: {count} questões")


def main():
    """Função principal do script."""
    extractor = EnemQuestionExtractor()
    
    # Verificar se a pasta quiz-items existe
    if not extractor.quiz_items_path.exists():
        print("❌ Pasta 'quiz-items' não encontrada!")
        return
    
    # Extrair todas as questões
    extractor.extract_all_questions()
    
    # Exibir estatísticas
    extractor.get_statistics()


if __name__ == "__main__":
    main()
