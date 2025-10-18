import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { FormsModule } from '@angular/forms';
import { NgIf } from '@angular/common';
import { AuthService, UserInfo } from '../shared/admin.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  template: `
    <router-outlet></router-outlet>
  `
})
export class AppComponent {
  title = 'school-management';
  
  isLoggedIn = false;
  studentId: string | null = null;
  errorMessage = '';
  
  loginData = {
    userId: '',
    password: ''
  };
  
  constructor(private authService: AuthService) {}
  
  ngOnInit(): void {
    // 检查用户是否已经登录
    this.authService.getCurrentUser().subscribe({
      next: (user: UserInfo | null) => {
        if (user && user.role === 'student') {
          this.isLoggedIn = true;
          this.studentId = user.user_id;
        }
      },
      error: () => {
        // 忽略错误，用户可能未登录
      }
    });
  }
  
  onLogin(): void {
    this.errorMessage = '';
    
    this.authService.login(this.loginData.userId, this.loginData.password).subscribe({
      next: (user: UserInfo) => {
        if (user.role === 'student') {
          this.isLoggedIn = true;
          this.studentId = user.user_id;
          // 登录成功后可以考虑跳转到仪表板或其他页面
          // 如果有路由需要在这里添加router.navigate()
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