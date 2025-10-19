import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { BaseService, ApiResponse } from './base-service';

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

  getCurrentUser(): Observable<UserInfo | null> {
    return this.get<UserInfo>('me').pipe(
      map(response => {
        this.currentUserSubject.next(response);
        return response;
      }),
      catchError((error) => {
        if (error.status === 401) {
          this.currentUserSubject.next(null);
          return of(null);
        }
        return of(null); // 其他错误也返回 null，不影响用户体验
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