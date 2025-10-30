import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { BaseService } from './base-service';
import { Teacher, StudentScore, Class, Student } from './models';

interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
  timestamp: string;
}

@Injectable({
  providedIn: 'root'
}

)
export class TeacherService extends BaseService {
  protected override baseUrl = '/api/teacher'; // 使用代理URL

  constructor(http: HttpClient) {
    super(http);
  }

  /**
   * 获取教师个人资料
   * @param teacherId 教师ID
   */
  getTeacherProfile(teacherId: number): Observable<Teacher> {
    return this.getOne<Teacher>(`profile/${teacherId}`);
  }

  /**
   * 获取教师管理的学生成绩列表
   * @param teacherId 教师ID
   */
  getTeacherScores(teacherId: number): Observable<StudentScore[]> {
    // 通过设置per_page参数为一个足够大的数来获取所有数据
    return this.get<any>(`scores/${teacherId}?per_page=10000`)
      .pipe(
        map(response => response.scores),
        map(scores => scores.map((score: any) => ({
          score_id: Number(score.score_id),
          student_id: score.student_id,
          student_name: score.student_name,
          student_number: score.student_number,
          class_name: score.class_name,
          subject_id: Number(score.subject_id),
          subject_name: score.subject_name,
          exam_type_id: Number(score.exam_type_id),
          exam_name: score.exam_name,
          score: Number(score.score)
        })))
      );
  }

  /**
   * 更新学生成绩
   * @param teacherId 教师ID
   * @param scoreId 成绩ID
   * @param score 新成绩
   */
  updateStudentScore(teacherId: number, scoreId: number, score: number): Observable<StudentScore> {
    return this.put<StudentScore>(`scores/${teacherId}/${scoreId}`, { score })
      .pipe(
        map(scoreData => ({
          score_id: Number(scoreData.score_id),
          student_id: scoreData.student_id,
          student_name: scoreData.student_name,
          student_number: scoreData.student_number,
          class_name: scoreData.class_name,
          subject_id: Number(scoreData.subject_id),
          subject_name: scoreData.subject_name,
          exam_type_id: Number(scoreData.exam_type_id),
          exam_name: scoreData.exam_name,
          score: Number(scoreData.score)
        })),
        catchError(this.handleError)
      );
  }

  /**
   * 获取教师管理的班级列表
   * @param teacherId 教师ID
   */
  getTeacherClasses(teacherId: number): Observable<Class[]> {
    return this.get<any>(`classes/${teacherId}`)
      .pipe(
        map(response => response.classes),
        map(classes => classes.map((cls: any) => ({
          class_id: Number(cls.class_id),
          class_name: cls.class_name,
          teacher_name: cls.teacher_name || ''
        })))
      );
  }

  /**
   * 获取教师管理的学生列表
   * @param teacherId 教师ID
   */
  getTeacherStudents(teacherId: number): Observable<Student[]> {
    return this.get<any>(`students/${teacherId}`)
      .pipe(
        map(response => response.students),
        map(students => students.map((student: any) => ({
          student_id: student.student_id,
          student_name: student.student_name,
          class_name: student.class_name
        })))
      );
  }

  /**
   * 获取指定班级的学生列表
   * @param teacherId 教师ID
   * @param classId 班级ID
   */
  getClassStudents(teacherId: number, classId: string): Observable<Student[]> {
    return this.get<any>(`students/${teacherId}/class/${classId}`)
      .pipe(
        map(response => response.students),
        map(students => students.map((student: any) => ({
          student_id: student.student_id,
          student_name: student.student_name,
          class_name: student.class_name
        })))
      );
  }

  /**
   * 获取指定学生信息
   * @param teacherId 教师ID
   * @param studentId 学生ID
   */
  getTeacherStudent(teacherId: number, studentId: string): Observable<Student> {
    return this.getOne<Student>(`students/${teacherId}/${studentId}`);
  }
}