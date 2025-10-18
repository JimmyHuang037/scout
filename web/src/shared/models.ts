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
  teacher_id: string;
  teacher_name: string;
  subject_name: string;
  class_name: string;
}

// 管理员相关模型
export interface Admin {
  admin_id: string;
  admin_name: string;
}