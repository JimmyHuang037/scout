import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { NgIf } from '@angular/common';
import { AuthService, UserInfo } from '../shared/admin.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, NgIf],
  template: `
    <div class="login-container">
      <div class="login-form">
        <h2>学生管理系统登录</h2>
        <form (ngSubmit)="onLogin()" #loginForm="ngForm">
          <div class="form-group">
            <label for="userId">用户ID:</label>
            <input type="text" id="userId" name="userId" [(ngModel)]="loginData.userId" required />
          </div>
          
          <div class="form-group">
            <label for="password">密码:</label>
            <input type="password" id="password" name="password" [(ngModel)]="loginData.password" required />
          </div>
          
          <button type="submit" [disabled]="!loginForm.form.valid">登录</button>
          
          <div *ngIf="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </form>
      </div>
    </div>
  `,
  styles: [`
    .login-container {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: #f5f5f5;
    }
    
    .login-form {
      background: white;
      padding: 2rem;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      width: 100%;
      max-width: 400px;
    }
    
    .form-group {
      margin-bottom: 1rem;
    }
    
    label {
      display: block;
      margin-bottom: 0.5rem;
      font-weight: bold;
    }
    
    input {
      width: 100%;
      padding: 0.5rem;
      border: 1px solid #ddd;
      border-radius: 4px;
      box-sizing: border-box;
    }
    
    button {
      width: 100%;
      padding: 0.75rem;
      background-color: #3f51b5;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 1rem;
    }
    
    button:disabled {
      background-color: #cccccc;
      cursor: not-allowed;
    }
    
    button:hover:not(:disabled) {
      background-color: #303f9f;
    }
    
    .error-message {
      color: #f44336;
      margin-top: 1rem;
      text-align: center;
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
          this.router.navigate(['/dashboard'], { 
            queryParams: { studentId: this.loginData.userId } 
          });
        } else {
          this.errorMessage = '只有学生可以访问此系统';
          this.authService.logout().subscribe();
        }
      },
      error: (err: any) => {
        this.errorMessage = '登录失败：用户名或密码错误';
      }
    });
  }
}