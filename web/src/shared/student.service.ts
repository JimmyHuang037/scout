import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { Student, Score, ExamResult } from './models';

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
    return this.http.get(`${this.baseUrl}/exam_results/${studentId}`, { responseType: 'text' })
      .pipe(
        map(response => {
          // 检查响应是否为HTML（错误页面）
          if (response.startsWith('<!doctype') || response.startsWith('<html')) {
            throw new Error('Received HTML response instead of JSON. Check if the API server is running and the endpoint is correct.');
          }
          
          // 解析JSON响应
          const parsedResponse: ApiResponse<any[]> = JSON.parse(response);
          
          // 转换字符串类型字段为数字类型
          const examResults: ExamResult[] = parsedResponse.data.map(item => ({
            exam_name: item.exam_name,
            student_name: item.student_name,
            chinese: Number(item.chinese),
            math: Number(item.math),
            english: Number(item.english),
            physics: Number(item.physics),
            chemistry: Number(item.chemistry),
            politics: Number(item.politics),
            total_score: Number(item.total_score),
            ranking: Number(item.ranking)
          }));
          
          return examResults;
        }),
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse | Error) {
    let errorMessage = '';
    
    if (error instanceof HttpErrorResponse) {
      if (error.error instanceof ErrorEvent) {
        // 客户端错误
        errorMessage = `客户端错误: ${error.error.message}`;
      } else {
        // 服务器端错误
        errorMessage = `服务器返回代码 ${error.status}: ${error.message}`;
      }
    } else {
      // 解析错误或其他错误
      errorMessage = `解析错误: ${error.message}`;
    }
    
    console.error(errorMessage);
    // 返回错误信息而不是抛出错误，这样组件可以显示错误但不会中断其他请求
    return throwError(() => errorMessage);
  }
}