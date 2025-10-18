import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { Student, Score, ExamResult } from './student.model';

// 定义API响应接口
interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
  timestamp: string;
}

@Injectable({
  providedIn: 'root'
})
export class StudentService {
  private baseUrl = '/api/student'; // 使用代理URL

  constructor(private http: HttpClient) { }

  getStudentProfile(studentId: string): Observable<Student> {
    return this.http.get<ApiResponse<Student>>(`${this.baseUrl}/profile/${studentId}`)
      .pipe(
        map(response => response.data),
        catchError(this.handleError)
      );
  }

  getStudentScores(studentId: string): Observable<Score[]> {
    return this.http.get<ApiResponse<Score[]>>(`${this.baseUrl}/scores/${studentId}`)
      .pipe(
        map(response => response.data),
        catchError(this.handleError)
      );
  }

  getStudentExamResults(studentId: string): Observable<ExamResult[]> {
    return this.http.get<ApiResponse<ExamResult[]>>(`${this.baseUrl}/exam_results/${studentId}`)
      .pipe(
        map(response => response.data),
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = '';
    if (error.error instanceof ErrorEvent) {
      // 客户端错误
      errorMessage = `客户端错误: ${error.error.message}`;
    } else {
      // 服务器端错误
      errorMessage = `服务器返回代码 ${error.status}: ${error.message}`;
    }
    console.error(errorMessage);
    return throwError(() => errorMessage);
  }
}