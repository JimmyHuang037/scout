export interface Student {
  student_id: string;
  name: string;
  class_name: string;
  enrollment_year: number;
}

export interface Score {
  subject_name: string;
  exam_type_name: string;
  score: number;
  exam_date: string;
}

export interface ExamResult {
  subject_name: string;
  exam_type_name: string;
  rank: number;
  max_score: number;
  average_score: number;
  exam_date: string;
}