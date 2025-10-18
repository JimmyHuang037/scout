import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private baseUrl = '/api/admin'; // 使用代理URL

  constructor(private http: HttpClient) { }

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
    return throwError(() => errorMessage);
  }
}