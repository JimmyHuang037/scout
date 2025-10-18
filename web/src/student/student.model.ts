export interface Student {
  student_id: string;
  student_name: string;
  class_name: string;
}

export interface Score {
  score_id: number;
  score: number;
  exam_name: number | string;
  subject_name: number | string;
  student_name: string;
}

export interface ExamResult {
  exam_name: string;
  student_name: string;
  chinese: string;
  math: string;
  english: string;
  physics: string;
  chemistry: string;
  politics: string;
  total_score: string;
  ranking: number;
}