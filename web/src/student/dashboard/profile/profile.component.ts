import { Component, Input } from '@angular/core';
import { Student } from '../../shared/student.model';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [NgIf],
  template: `
    <div class="section">
      <h3>个人信息</h3>
      <div class="info-grid" *ngIf="student">
        <div class="info-item">
          <span class="label">姓名:</span>
          <span>{{student.student_name}}</span>
        </div>
        <div class="info-item">
          <span class="label">学号:</span>
          <span>{{student.student_id}}</span>
        </div>
        <div class="info-item">
          <span class="label">班级:</span>
          <span>{{student.class_name}}</span>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .section {
      margin-bottom: 30px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      padding: 20px;
    }

    .section h3 {
      margin-top: 0;
      color: #333;
      border-bottom: 2px solid #3f51b5;
      padding-bottom: 10px;
    }

    .info-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 15px;
    }

    .info-item {
      display: flex;
      flex-direction: column;
    }

    .label {
      font-weight: bold;
      color: #555;
    }
  `]
})
export class ProfileComponent {
  @Input() student: Student | null = null;
}