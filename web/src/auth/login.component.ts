import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { NgIf } from '@angular/common';
import { AuthService, UserInfo } from '../shared/admin.service';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatToolbarModule } from '@angular/material/toolbar';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    FormsModule, 
    NgIf,
    MatCardModule,
    MatInputModule,
    MatButtonModule,
    MatFormFieldModule,
    MatToolbarModule
  ],
  template: `
    <div class="login-container">
      <mat-toolbar color="primary">
        <span>学生管理系统</span>
      </mat-toolbar>
      
      <mat-card class="login-card">
        <mat-card-header>
          <mat-card-title>用户登录</mat-card-title>
        </mat-card-header>
        
        <mat-card-content>
          <form (ngSubmit)="onLogin()" #loginForm="ngForm">
            <mat-form-field appearance="fill" class="full-width">
              <mat-label>用户ID</mat-label>
              <input matInput type="text" name="userId" [(ngModel)]="loginData.userId" required />
            </mat-form-field>
            
            <mat-form-field appearance="fill" class="full-width">
              <mat-label>密码</mat-label>
              <input matInput type="password" name="password" [(ngModel)]="loginData.password" required />
            </mat-form-field>
            
            <button 
              mat-raised-button 
              color="primary" 
              type="submit" 
              [disabled]="!loginForm.form.valid"
              class="login-button">
              登录
            </button>
            
            <div *ngIf="errorMessage" class="error-message">
              <p class="mat-error">{{ errorMessage }}</p>
            </div>
          </form>
        </mat-card-content>
      </mat-card>
    </div>
  `,
  styles: [`
    .login-container {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: #f5f5f5;
      padding: 20px;
    }
    
    .login-card {
      width: 100%;
      max-width: 400px;
      margin-top: 20px;
    }
    
    .full-width {
      width: 100%;
      margin-bottom: 1rem;
    }
    
    .login-button {
      width: 100%;
      padding: 0.75rem;
      font-size: 1rem;
    }
    
    .error-message {
      margin-top: 1rem;
      text-align: center;
    }
    
    mat-toolbar {
      width: 100%;
      max-width: 400px;
      border-radius: 4px;
      justify-content: center;
    }
  `]
})
export class LoginComponent {
  errorMessage = '';
  
  loginData = {
    userId: '',
    password: ''
  };
  
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}
  
  onLogin(): void {
    this.errorMessage = '';
    
    this.authService.login(this.loginData.userId, this.loginData.password).subscribe({
      next: (user: UserInfo) => {
        if (user.role === 'student') {
          this.router.navigate(['/student/dashboard'], { 
            queryParams: { studentId: this.loginData.userId } 
          });
        } else if (user.role === 'teacher') {
          this.router.navigate(['/teacher/dashboard'], { 
            queryParams: { teacherId: this.loginData.userId } 
          });
        } else if (user.role === 'admin') {
          this.router.navigate(['/admin/dashboard'], { 
            queryParams: { adminId: this.loginData.userId } 
          });
        } else {
          this.errorMessage = '不支持的用户角色';
          this.authService.logout().subscribe();
        }
      },
      error: (err: any) => {
        this.errorMessage = '登录失败：用户名或密码错误';
      }
    });
  }
}