import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { BaseService, ApiResponse } from './base-service';
import { Student, Teacher, Class, Subject, ExamType } from './models';

// 定义用户信息接口
export interface UserInfo {
  user_id: string;
  username: string;
  role: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService extends BaseService {
  protected override baseUrl = '/api/auth';
  
  private currentUserSubject = new BehaviorSubject<UserInfo | null>(null);
  public currentUser = this.currentUserSubject.asObservable();

  constructor(http: HttpClient) {
    super(http);
  }

  login(userId: string, password: string): Observable<UserInfo> {
    return this.post<UserInfo>('login', { user_id: userId, password }).pipe(
      map(response => {
        this.currentUserSubject.next(response);
        return response;
      })
    );
  }

  getCurrentUser(): Observable<UserInfo> {
    return this.getOne<UserInfo>('me').pipe(
      map(response => {
        this.currentUserSubject.next(response);
        return response;
      })
    );
  }

  logout(): Observable<any> {
    return this.post('logout', {}).pipe(
      map(response => {
        this.currentUserSubject.next(null);
        return response;
      })
    );
  }
  
  getUserRole(): string | null {
    const user = this.currentUserSubject.value;
    return user ? user.role : null;
  }
  
  getUserId(): string | null {
    const user = this.currentUserSubject.value;
    return user ? user.user_id : null;
  }
}

@Injectable({
  providedIn: 'root'
})
export class AdminService extends BaseService {
  protected override baseUrl = '/api/admin'; // 使用代理URL

  constructor(http: HttpClient) {
    super(http);
  }

  // 学生管理相关方法
  getStudents(): Observable<Student[]> {
    return this.http.get<ApiResponse<{students: Student[]}>>(`${this.baseUrl}/students`)
      .pipe(
        map(response => response.data.students),
        catchError(this.handleError)
      );
  }

  getStudent(studentId: string): Observable<Student> {
    return this.getOne<Student>(`students/${studentId}`);
  }

  createStudent(student: Partial<Student>): Observable<Student> {
    return this.post<Student>('students', student);
  }

  updateStudent(studentId: string, student: Partial<Student>): Observable<Student> {
    return this.put<Student>(`students/${studentId}`, student);
  }

  deleteStudent(studentId: string): Observable<any> {
    return this.delete(`students/${studentId}`);
  }

  // 教师管理相关方法
  getTeachers(): Observable<Teacher[]> {
    return this.http.get<ApiResponse<{teachers: Teacher[]}>>(`${this.baseUrl}/teachers`)
      .pipe(
        map(response => response.data.teachers),
        catchError(this.handleError)
      );
  }

  getTeacher(teacherId: number): Observable<Teacher> {
    return this.getOne<Teacher>(`teachers/${teacherId}`);
  }

  createTeacher(teacher: Partial<Teacher>): Observable<Teacher> {
    return this.post<Teacher>('teachers', teacher);
  }

  updateTeacher(teacherId: number, teacher: Partial<Teacher>): Observable<Teacher> {
    return this.put<Teacher>(`teachers/${teacherId}`, teacher);
  }

  deleteTeacher(teacherId: number): Observable<any> {
    return this.delete(`teachers/${teacherId}`);
  }

  // 班级管理相关方法
  getClasses(): Observable<Class[]> {
    return this.http.get<ApiResponse<{classes: Class[]}>>(`${this.baseUrl}/classes`)
      .pipe(
        map(response => response.data.classes),
        catchError(this.handleError)
      );
  }

  getClass(classId: number): Observable<Class> {
    return this.getOne<Class>(`classes/${classId}`);
  }

  createClass(cls: Partial<Class>): Observable<Class> {
    return this.post<Class>('classes', cls);
  }

  updateClass(classId: number, cls: Partial<Class>): Observable<Class> {
    return this.put<Class>(`classes/${classId}`, cls);
  }

  deleteClass(classId: number): Observable<any> {
    return this.delete(`classes/${classId}`);
  }

  // 科目管理相关方法
  getSubjects(): Observable<Subject[]> {
    return this.http.get<ApiResponse<{subjects: Subject[]}>>(`${this.baseUrl}/subjects`)
      .pipe(
        map(response => response.data.subjects),
        catchError(this.handleError)
      );
  }

  getSubject(subjectId: number): Observable<Subject> {
    return this.getOne<Subject>(`subjects/${subjectId}`);
  }

  createSubject(subject: Partial<Subject>): Observable<Subject> {
    return this.post<Subject>('subjects', subject);
  }

  updateSubject(subjectId: number, subject: Partial<Subject>): Observable<Subject> {
    return this.put<Subject>(`subjects/${subjectId}`, subject);
  }

  deleteSubject(subjectId: number): Observable<any> {
    return this.delete(`subjects/${subjectId}`);
  }

  // 考试类型管理相关方法
  getExamTypes(): Observable<ExamType[]> {
    return this.http.get<ApiResponse<{exam_types: ExamType[]}>>(`${this.baseUrl}/exam_types`)
      .pipe(
        map(response => response.data.exam_types),
        catchError(this.handleError)
      );
  }

  getExamType(examTypeId: number): Observable<ExamType> {
    return this.getOne<ExamType>(`exam_types/${examTypeId}`);
  }

  createExamType(examType: Partial<ExamType>): Observable<ExamType> {
    return this.post<ExamType>('exam_types', examType);
  }

  updateExamType(examTypeId: number, examType: Partial<ExamType>): Observable<ExamType> {
    return this.put<ExamType>(`exam_types/${examTypeId}`, examType);
  }

  deleteExamType(examTypeId: number): Observable<any> {
    return this.delete(`exam_types/${examTypeId}`);
  }
}