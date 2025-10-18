import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-admin-root',
  standalone: true,
  imports: [RouterOutlet],
  template: `
    <div class="main-container">
      <h1>管理员系统</h1>
      <p>管理员功能正在开发中...</p>
    </div>
  `,
  styles: [`
    .main-container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }
    
    h1 {
      text-align: center;
      color: #3f51b5;
    }
  `]
})
export class AdminAppComponent {
  title = 'school-management';
}