import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, DashboardComponent],
  template: `
    <div class="main-container">
      <h1>学生管理系统</h1>
      <app-dashboard></app-dashboard>
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
export class AppComponent {
  title = 'student-portal';
}