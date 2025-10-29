// 学生相关模型
export interface Student {
  student_id: string;
  student_name: string;
  class_name: string;
}

export interface Score {
  score_id: number;
  score: number;
  exam_name: string;
  subject_name: string;
  student_name: string;
}

export interface ExamResult {
  exam_name: string;
  student_name: string;
  chinese: number;
  math: number;
  english: number;
  physics: number;
  chemistry: number;
  politics: number;
  total_score: number;
  ranking: number;
}

// 教师相关模型
export interface Teacher {
  teacher_id: number;
  teacher_name: string;
}

// 管理员相关模型
export interface Class {
  class_id: number;
  class_name: string;
  teacher_name: string;
}

export interface Subject {
  subject_id: number;
  subject_name: string;
}

export interface ExamType {
  exam_type_id: number;
  exam_name: string;
}

export interface StudentScore {
  score_id: number;
  student_id: string;
  student_name: string;
  student_number: string;
  class_name: string;
  subject_id: number;
  subject_name: string;
  exam_type_id: number;
  exam_name: string;
  score: number;
}
