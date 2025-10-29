import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BaseService } from './base-service';
import { Teacher, StudentScore, Class, Student } from './models';

@Injectable({
  providedIn: 'root'
})
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
    return this.getList<StudentScore>(`scores/${teacherId}`);
  }

  /**
   * 更新学生成绩
   * @param teacherId 教师ID
   * @param scoreId 成绩ID
   * @param score 新成绩
   */
  updateStudentScore(teacherId: number, scoreId: number, score: number): Observable<StudentScore> {
    return this.post<StudentScore>(`scores/${teacherId}/${scoreId}`, { score });
  }

  /**
   * 获取教师管理的班级列表
   * @param teacherId 教师ID
   */
  getTeacherClasses(teacherId: number): Observable<Class[]> {
    return this.getList<Class>(`classes/${teacherId}`);
  }

  /**
   * 获取教师管理的学生列表
   * @param teacherId 教师ID
   */
  getTeacherStudents(teacherId: number): Observable<Student[]> {
    return this.getList<Student>(`students/${teacherId}`);
  }

  /**
   * 获取指定班级的学生列表
   * @param teacherId 教师ID
   * @param classId 班级ID
   */
  getClassStudents(teacherId: number, classId: string): Observable<Student[]> {
    return this.getList<Student>(`students/${teacherId}/class/${classId}`);
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