import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError, BehaviorSubject, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

// 定义API响应接口
interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
  timestamp: string;
}

// 定义用户信息接口
export interface UserInfo {
  user_id: string;
  username: string;
  role: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private baseUrl = '/api/auth';
  
  private currentUserSubject = new BehaviorSubject<UserInfo | null>(null);
  public currentUser = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) { }

  login(userId: string, password: string): Observable<UserInfo> {
    return this.http.post<ApiResponse<UserInfo>>(`${this.baseUrl}/login`, { user_id: userId, password })
      .pipe(
        map(response => {
          this.currentUserSubject.next(response.data);
          return response.data;
        }),
        catchError(this.handleError)
      );
  }

  getCurrentUser(): Observable<UserInfo | null> {
    return this.http.get<ApiResponse<UserInfo>>(`${this.baseUrl}/me`)
      .pipe(
        map(response => {
          this.currentUserSubject.next(response.data);
          return response.data;
        }),
        catchError((error: HttpErrorResponse) => {
          // 如果是未登录错误，则返回null
          if (error.status === 401) {
            this.currentUserSubject.next(null);
            return of(null);
          }
          return this.handleError(error);
        })
      );
  }

  logout(): Observable<any> {
    return this.http.post<ApiResponse<any>>(`${this.baseUrl}/logout`, {})
      .pipe(
        map(response => {
          this.currentUserSubject.next(null);
          return response;
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
  
  getUserRole(): string | null {
    const user = this.currentUserSubject.value;
    return user ? user.role : null;
  }
  
  getUserId(): string | null {
    const user = this.currentUserSubject.value;
    return user ? user.user_id : null;
  }
}