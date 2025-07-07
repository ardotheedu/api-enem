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
    filePath?: string;
    isCorrect: boolean;
  }[];
  files: string[];
}
