export interface QuestionDto {
  id: number;
  title: string;
  index: number;
  year: number;
  context?: string;
  alternativesIntroduction?: string;
  correctAlternative?: string;
  discipline?: {
    label: string;
    value: string;
  } | null;
  language?: {
    label: string;
    value: string;
  } | null;
  alternatives: {
    letter: string;
    text: string;
    file?: string; // Compatibilidade com nome original
    filePath?: string;
    isCorrect: boolean;
  }[];
  files: string[];
  images?: {
    context: string[]; // Imagens extraídas do contexto
    files: string[]; // Arquivos de imagem da questão
    alternatives: {
      letter: string;
      filePath: string;
    }[]; // Imagens das alternativas
  };
}
